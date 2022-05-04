from django.forms import ModelForm
from pipelines.models import Group

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('key', 'window',)