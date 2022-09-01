from django.contrib.auth.models import AbstractUser as DjangoUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import Account

class User(DjangoUser):

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	username = None
	email = models.EmailField(_("email address"), unique=True)
	account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('account'), related_name='users')