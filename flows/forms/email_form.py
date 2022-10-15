from django.forms import ModelForm
from flows.models import Email

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ('subject', 'html_body', 'text_body', 'autogenerate_text', 'from_email', 'preview_context',)
