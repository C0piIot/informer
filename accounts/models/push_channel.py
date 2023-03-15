import firebase_admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from firebase_admin import messaging

from .channel import Channel


class PushChannel(Channel):
    class Meta:
        verbose_name = _("push channel")
        verbose_name_plural = _("push channels")

    ICON = "🔔"
    CONTACT_FORM = "accounts.forms.PushContactForm"
    CONTACT_SERIALIZER = "accounts.serializers.PushContactSerializer"
    CONFIG_FORM = "accounts.forms.PushChannelForm"
    firebase_credentials = models.JSONField(
        _("Firebase credentials"), default=dict)

    def firebase_app_name(self):
        return f"firebase-app-{self.site.pk}"

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not exclude or not "firebase_credentials" in exclude:
            if self.firebase_credentials:
                try:
                    firebase_admin.delete_app(
                        firebase_admin.get_app(name=self.firebase_app_name())
                    )
                except:
                    pass
                try:
                    self.get_firebase()
                except ValueError as err:
                    raise ValidationError({"firebase_credentials": _(
                        f"The firebase credentials data doen't seems to be correct: {err}")})

    def get_firebase(self):
        try:
            return firebase_admin.get_app(name=self.firebase_app_name())
        except ValueError:
            return firebase_admin.initialize_app(
                firebase_admin.credentials.Certificate(
                    self.firebase_credentials),
                name=self.firebase_app_name(),
            )

    def send_push(self, title, body, url, tokens):
        response = messaging.send_multicast(
            messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                tokens=tokens,
            ),
            app=self.get_firebase(),
        )

        return {tokens[i]: r.success for i, r in enumerate(response.responses)}
