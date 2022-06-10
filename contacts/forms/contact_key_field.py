from rest_framework import serializers
from django.utils.module_loading import import_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ContactKeyField(serializers.Field):

    default_error_messages = {
        'incorrect_key': _('There is no contact with the supplied key')
    }

    def to_representation(self, value):
        return value.key

    def to_internal_value(self, data):
        if contact := import_string(settings.CONTACT_STORAGE).get_model(self.context['environment'], data):
            return contact

        self.fail('incorrect_key')