"""
    flaskapp.api.admin.token
    ~~~~~~~~~~~~~~

    Token endpoints
"""

from flask import Flask, Blueprint, request, current_app, jsonify, make_response
from flask_restful import Resource, Api, abort, reqparse
from wscodec.decoder.exceptions import *
from sqlalchemy.exc import IntegrityError
import requests
from ...services import captures, tags
from ...captures.schemas import ConsumerCaptureSchema, ConsumerCaptureSchemaWithSamples
from ..baseresource import SingleResource, MultipleResource
import jwt
from datetime import datetime, timedelta
from secrets import token_hex
from ...config import TAGTOKEN_CLIENTID, TAGTOKEN_CLIENTSECRET
from json import dumps

bp = Blueprint('captures', __name__)
api = Api(bp)


class Capture(SingleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def delete(self, id):
        abort(404)


class Captures(MultipleResource):
    def __init__(self):
        super().__init__(ConsumerCaptureSchema, captures)

    def createtoken(self, tagserial:str):
        """ Inspired by https://h.readthedocs.io/en/latest/publishers/authorization-grant-tokens/#python """
        now = datetime.utcnow()

        payload = {
            'aud': tagserial,
            'iss': TAGTOKEN_CLIENTID,
            'sub': token_hex(32),
            'nbf': now,
            'exp': now + timedelta(minutes=10),
        }

        return jwt.encode(payload, TAGTOKEN_CLIENTSECRET, algorithm='HS256')

    def webhooktx(self, tagobj, captureobj):
        """
        Transmit JSON dictionary to a webhook
        :param tagobj: Tag object
        :param captureobj: A capture object
        :return: None
        """
        webhook = tagobj.webhook
        if webhook is None:
            return

        schema = ConsumerCaptureSchemaWithSamples()
        capturedict = schema.dump(captureobj)

        #https://webhook.site/a1b658b6-6b23-4a49-959c-e9b33d20e074
        print(webhook.address)
        req = requests.post(webhook.address, json=capturedict, timeout=10)


    def get(self):
        """
        Get a list of captures for a tag
        """
        parsedargs = Captures.parse_body_args(request.args.to_dict(),
                                              requiredlist=['serial'],
                                              optlist=['offset', 'limit'])

        serial = parsedargs['serial']
        offset = parsedargs.get('offset', 0)
        limit = parsedargs.get('limit', None)

        tagobj = tags.get_by_serial(serial)
        capturelist = captures.find(parent_tag=tagobj).order_by(captures.__model__.timestamp.desc()).offset(offset).limit(limit)

        schema = self.Schema()
        result = schema.dump(capturelist, many=True)
        return jsonify(result)

    def post(self):
        """
        Create a capture
        """
        parsedargs = super().parse_body_args(request.get_json(),
                                              requiredlist=['serial', 'statusb64', 'timeintb64', 'circbufb64', 'vfmtb64'])

        tagobj = tags.get_by_serial(parsedargs['serial'])

        try:
            captureobj = captures.decode_and_create(tagobj=tagobj,
                                                    statb64=parsedargs['statusb64'],
                                                    timeintb64=parsedargs['timeintb64'],
                                                    circb64=parsedargs['circbufb64'],
                                                    vfmtb64=parsedargs['vfmtb64'])

            tagtoken = self.createtoken(tagserial=tagobj.serial).decode('utf-8')
            tagtoken_type = 'Bearer'

            schema = self.Schema()
            capturedict = schema.dump(captureobj)

            # If the tag has a webhook post to this.
            self.webhooktx(tagobj, captureobj)

            capturedict.update({'tagtoken': tagtoken})
            capturedict.update({'tagtoken_type': tagtoken_type})
            return jsonify(capturedict)

        except InvalidMajorVersionError as e:
            return make_response(jsonify(ecode=101, description=str(e),
                                 encoderversion=e.encoderversion, decoderversion=e.decoderversion), 422)

        except InvalidFormatError as e:
            return make_response(jsonify(ecode=102, description=str(e), circformat=e.circformat), 422)

        except MessageIntegrityError as e:
            return make_response(jsonify(ecode=103, description=str(e), urlhash=e.urlhash, calchash=e.calchash), 401)

        except NoCircularBufferError as e:
            return make_response(jsonify(ecode=104, description=str(e), status=e.status), 400)

        except DelimiterNotFoundError as e:
            return make_response(jsonify(ecode=105, description=str(e), status=e.status, circb64=e.circb64), 422)

        except IntegrityError as e:
            return make_response(jsonify(ecode=106, description=str(e)), 409)


api.add_resource(Capture, '/captures/<id>')
api.add_resource(Captures, '/captures')
