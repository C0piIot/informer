from django.forms import ModelForm

from flows.models import Webhook


class WebhookForm(ModelForm):
    class Meta:
        model = Webhook
        fields = ("url", "method", "contenttype", "body", "skip_ssl")
