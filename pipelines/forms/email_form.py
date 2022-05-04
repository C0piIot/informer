from django.forms import ModelForm
from pipelines.models import Email

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ('email_channel', 'subject', 'html_body', 'text_body', 'autogenerate_text', 'only_unread',)
