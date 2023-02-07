from django.core.exceptions import ValidationError
from django.core.mail import get_connection, send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from .channel import Channel


class EmailChannel(Channel):

    class Meta:
        verbose_name = _("email channel")
        verbose_name_plural = _("email channels")
    ICON = "✉️"
    CONTACT_FORM = "accounts.forms.EmailContactForm"
    CONTACT_SERIALIZER = "accounts.serializers.EmailContactSerializer"
    CONFIG_FORM = "accounts.forms.EmailChannelForm"
    SECURITY_NONE = "none"
    SECURITY_TSL_SSL = "ssl"
    SECURITY_STARTTLS = "starttls"
    SECURITY_CHOICES = (
        (SECURITY_NONE, _("None")),
        (SECURITY_TSL_SSL, _("TSL/SSL")),
        (SECURITY_STARTTLS, _("STARTTLS")),
    )

    host = models.CharField(_("host"), max_length=100)
    port = models.PositiveSmallIntegerField(_("port"))
    username = models.CharField(_("username"), max_length=150)
    password = models.CharField(_("password"), max_length=150)
    security = models.CharField(
        _("security"), max_length=20, choices=SECURITY_CHOICES, default=SECURITY_TSL_SSL
    )
    from_email = models.EmailField(
        _("from email"),
        max_length=200,
        help_text=_("Default from address for this channel"),
    )

    def send_mail(self, subject, message, html_message, from_email, recipient):
        send_mail(
            subject,
            message,
            from_email,
            [recipient],
            connection=self.get_connection(),
            html_message=html_message,
        )

    def get_connection(self):
        return get_connection(
            "django.core.mail.backends.smtp.EmailBackend",
            fail_silently=False,
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=self.security == self.SECURITY_STARTTLS,
            use_ssl=self.security == self.SECURITY_TSL_SSL,
        )
