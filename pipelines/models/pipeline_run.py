from django.db import models
from django.utils.translation import gettext_lazy as _

class PipelineRun(models.Model):
    event = models.CharField(_('event'), max_length=200)
    contact_key = models.CharField(_('contact key'), max_length=100,)
    event_payload = models.JSONField(_('event payload'), default=dict)
    pipeline_data = models.JSONField(_('pipeline data'), default=dict)


    def next_step(current_step):
        pass


    @classmethod
    def get_contacts(cls, environment, start_key=None, amount=50, **filters):
        pass

    @classmethod
    def get_contact(cls, environment, key):
        pass

    @classmethod
    def save_contact(cls, environment, contact):
        pass

    @classmethod
    def delete_contact(cls, environment, key):
        pass