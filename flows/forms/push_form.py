from django.forms import ModelForm
from flows.models import Push

class PushForm(ModelForm):
    class Meta:
        model = Push
        fields = ('title', 'body', 'url', 'testing_context',)
