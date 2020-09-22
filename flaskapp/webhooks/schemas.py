from ..core import db
from .models import Webhook

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

# http://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html

__all__ = ['WebhookSchema', 'ConsumerWebhookSchemaWithKey', 'ConsumerWebhookSchema']


class WebhookSchema(ModelSchema):
    class Meta:
        model = Webhook
        sqla_session = db.session
        strict = True
    tag_id = fields.Integer()
    created_on = fields.DateTime(dump_only=True)


class ConsumerWebhookSchemaWithKey(WebhookSchema):
    class Meta(WebhookSchema.Meta):
        exclude = ('parent_tag',)
    tagserial = fields.String()
    created_on = fields.DateTime(dump_only=True)
    load_only = ('tag_id',)


class ConsumerWebhookSchema(ConsumerWebhookSchemaWithKey):
    class Meta(WebhookSchema.Meta):
        exclude = ('parent_tag', 'wh_secretkey',)




