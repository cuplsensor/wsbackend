# -*- coding: utf-8 -*-
"""
    flaskapp.api
    ~~~~~~~

    web api application package
"""

from functools import wraps
from ... import factory

from .version import bp as versionbp
from .tags import bp as tagsbp
from .captures import bp as capturesbp
from .samples import bp as samplesbp


def create_app(settings_override=None):
    """Returns the Web API application instance"""

    app = factory.create_api_app(__name__, __path__, settings_override)
    app.register_blueprint(versionbp)
    app.register_blueprint(tagsbp)
    app.register_blueprint(capturesbp)
    app.register_blueprint(samplesbp)

    return app
