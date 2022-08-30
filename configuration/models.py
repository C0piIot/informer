from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.core.mail import get_connection, send_mail
from django.urls import reverse
from django.core.exceptions import ValidationError
import firebase_admin
from firebase_admin import messaging

class Account(models.Model):
    name = models.CharField(_('name'), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')


class Environment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('account'), editable=False, related_name='environments')
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), editable=False)

    def get_absolute_url(self):
        return reverse('pipelines:list', kwargs={ 'environment': self.slug })

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(**kwargs)

    class Meta:
        unique_together = ('account', 'name')
        verbose_name = _('environment')
        verbose_name_plural = _('environments')


class Channel(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('account'), editable=False, related_name='channels')
    enabled = models.BooleanField(_('enabled'), default=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)

    def get_typed_instance(self):
        return getattr(self, self.content_type.model)

    def __str__(self):
        return self.get_typed_instance().__str__()


    def save(self, *args, **kwargs):
        if not self.content_type_id:
            content_type = ContentType.objects.get_for_model(self, for_concrete_model=True)
            if content_type.model_class() != Channel:
                self.content_type = content_type
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('account', 'content_type',)
        verbose_name = _('channel')
        verbose_name_plural = _('channels')
        unique_together = ('account', 'content_type',)

    def __str__(self):
        return self.content_type.name


class EmailChannel(Channel):
    SECURITY_NONE = 'none'
    SECURITY_TSL_SSL = 'ssl'
    SECURITY_STARTTLS = 'starttls'
    SECURITY_CHOICES = (
        (SECURITY_NONE, _('None')),
        (SECURITY_TSL_SSL, _('TSL/SSL')),
        (SECURITY_STARTTLS, _('STARTTLS')),
    )

    host = models.CharField(_('host'), max_length=100)
    port = models.PositiveSmallIntegerField(_('port'))
    username = models.CharField(_('username'), max_length=150)
    password = models.CharField(_('password'), max_length=150)
    security = models.CharField(_('security'),max_length=20, choices=SECURITY_CHOICES, default=SECURITY_TSL_SSL)
    from_email = models.EmailField(_('from email'), max_length=200, help_text=_('Default from address for this channel'))


    def send_mail(self, subject, message, html_message, from_email, recipient):
        send_mail(subject, message, from_email, [recipient], connection=self.get_connection(), html_message=html_message)


    def get_connection(self):
        return get_connection(
            'django.core.mail.backends.smtp.EmailBackend',
            fail_silently=False,
            host=self.host, 
            port=self.port, 
            username=self.username, 
            password=self.password, 
            use_tls=self.security == self.SECURITY_STARTTLS, 
            use_ssl=self.security == self.SECURITY_TSL_SSL
        )

    class Meta:
        verbose_name = _('email channel')
        verbose_name_plural = _('email channels')



class PushChannel(Channel):
    firebase_credentials = models.JSONField(_("Firebase credentials"), default=dict, blank=True)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not exclude or not 'firebase_credentials' in exclude:
            if self.firebase_credentials:
                try:
                    self.init_firebase()
                except ValueError as err:
                    raise ValidationError({
                        'firebase_credentials': _("The firebase credentials data doen't seems to be correct: %s" % err)
                    })


    def init_firebase(self):
        return firebase_admin.initialize_app(firebase_admin.credentials.Certificate(self.firebase_credentials))

    def send_push(self, title, body, url, tokens):
        firebase = self.init_firebase()
        
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