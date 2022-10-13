from django.db import models
from django.utils.translation import gettext_lazy as _
from .flow_step import FlowStep

class SendChannel(FlowStep):
	only_unread = models.BooleanField(_('unread only'), default=True, help_text=_("Send notification only if user have not seen it yet"))

	class Meta:
		abstract = True