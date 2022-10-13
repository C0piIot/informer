from django.forms import ModelForm
from flows.models import Email

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ('email_channel', 'subject', 'html_body', 'text_body', 'autogenerate_text', 'from_email', 'only_unread',)
