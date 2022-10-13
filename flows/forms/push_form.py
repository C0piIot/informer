from django.forms import ModelForm
from flows.models import Push

class PushForm(ModelForm):
    class Meta:
        model = Push
        fields = ('push_channel', 'title', 'body', 'url', 'only_unread',)
