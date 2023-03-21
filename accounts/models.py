import firebase_admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser as DjangoUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import get_connection, send_mail
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from firebase_admin import messaging
from rest_framework.authtoken.models import Token


class Channel(models.Model):
    class Meta:
        ordering = (
            "site",
            "content_type",
        )
        verbose_name = _("channel")
        verbose_name_plural = _("channels")
        unique_together = (
            "site",
            "content_type",
        )

    ICON = "🔊"
    CONTACT_FORM = None
    CONTACT_SERIALIZER = None
    CONFIG_FORM = None
    site = models.ForeignKey(
        Site, verbose_name=_("site"),
        on_delete=models.CASCADE, related_name="channels")
    enabled = models.BooleanField(_("enabled"), default=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False
    )

    def get_typed_instance(self):
        return getattr(self, self.content_type.model)

    def save(self, *args, **kwargs):
        if not self.content_type_id:
            content_type = ContentType.objects.get_for_model(
                self, for_concrete_model=True
            )
            if content_type.model_class() != Channel:
                self.content_type = content_type
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_typed_instance().ICON} {self.content_type.name}"


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
    security = models.CharField(_("security"),
                                max_length=20, choices=SECURITY_CHOICES,
                                default=SECURITY_TSL_SSL)
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
            connection=get_connection(),
            html_message=html_message,
        )


class Environment(models.Model):
    class Meta:
        unique_together = ("site", "name")
        verbose_name = _("environment")
        verbose_name_plural = _("environments")

    site = models.ForeignKey(
        Site,
        verbose_name=_("site"),
        on_delete=models.CASCADE,
        related_name="environments",
        editable=False,
    )
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("slug"), editable=False)
    private_key = models.CharField(_("private key"), max_length=40)
    public_key = models.CharField(_("public key"), max_length=40)

    def get_absolute_url(self):
        return reverse("stats:dashboard", kwargs={"environment": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.private_key:
            self.private_key = Token.generate_key()
        if not self.public_key:
            self.public_key = Token.generate_key()
        super().save(**kwargs)

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

    def __str__(self):
        return str(self.name)


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
                        f"The firebase credentials data doen't seems to be correct: {err}"
                    )}) from err

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


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, site, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = User(email=email, first_name=first_name,
                    site_id=site, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email, first_name, site, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            email, first_name, site, password, **extra_fields)

    def create_superuser(
            self, email, first_name, site, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(
            email, first_name, site, password, **extra_fields)


class User(DjangoUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "site"]

    objects = UserManager()

    username = None
    email = models.EmailField(_("email address"), unique=True)
    site = models.ForeignKey(
        Site, verbose_name=_("site"),
        on_delete=models.CASCADE, related_name="users")
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
