import re

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PushContactSerializer(serializers.Serializer):
    fcm_token_validation = re.compile("^[0-9A-Za-z_:-]{100,500}$")
    fcm_tokens = serializers.JSONField()

    def validate_fcm_tokens(self, value):
        if type(value) != list:
            raise serializers.ValidationError(
                _("fcm_tokens is expected to be a list"))

        for token in value:
            if not self.fcm_token_validation.match(token):
                raise serializers.ValidationError(_("Invalid fcm tokens"))
