from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from .channel import Channel
import firebase_admin
from firebase_admin import messaging


class PushChannel(Channel):
    
    firebase_credentials = models.JSONField(_("Firebase credentials"), default=dict)

    def firebase_app_name(self):
        return "firebase-app-%d" % self.site.pk

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not exclude or not 'firebase_credentials' in exclude:
            if self.firebase_credentials:
                try:
                    firebase_admin.delete_app(firebase_admin.get_app(name=self.firebase_app_name()))
                except:
                    pass
                try:
                    self.get_firebase()
                except ValueError as err:
                    raise ValidationError({
                        'firebase_credentials': _("The firebase credentials data doen't seems to be correct: %s" % err)
                    })


    def get_firebase(self):
        try:
            return firebase_admin.get_app(name=self.firebase_app_name())
        except ValueError:    
            return firebase_admin.initialize_app(firebase_admin.credentials.Certificate(self.firebase_credentials), name=self.firebase_app_name())

    def send_push(self, title, body, url, tokens):
        firebase = self.get_firebase()
        
        response = messaging.send_multicast(
            messaging.MulticastMessage(
                notification=messaging.Notification(
                   title=title,
                   body=body),
                tokens=tokens
            )
        )

        return { tokens[i]: r.success for i, r in enumerate(response.responses) } 
        

    class Meta:
        verbose_name = _('push channel')
        verbose_name_plural = _('push channels')