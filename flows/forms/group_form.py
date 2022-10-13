from django.forms import ModelForm
from flows.models import Group

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('key', 'window',)