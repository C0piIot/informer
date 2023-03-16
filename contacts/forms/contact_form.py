from django import forms
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from accounts.models import Channel
from contacts.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            "name",
            "key",
            "auth_key",
            "contact_data",
            "index1",
            "index2",
            "index3",
            "index4",
            "index5",
            "index6",
        )

    active_channel_tab = None
    CHANNEL_PREFIX = "channel-"
    environment = None
    channel_forms = None
    channels = forms.ModelMultipleChoiceField(
        required=False,
        label=_("Channels"),
        widget=forms.CheckboxSelectMultiple,
        queryset=Channel.objects.none(),
    )

    def __init__(self, **kwargs):
        self.environment = kwargs.pop("environment")
        super().__init__(**kwargs)
        channels = self.environment.site.channels.all()
        self.fields["channels"].queryset = channels
        if self.instance:
            self.fields["channels"].initial = channels.filter(
                content_type__model__in=self.instance.channel_data.keys()
            )
        self.channel_forms = {
            channel: import_string(channel.get_typed_instance().CONTACT_FORM)(
                prefix=f"{self.CHANNEL_PREFIX}{channel.pk}",
                data=kwargs.get("data"),
                files=kwargs.get("files"),
                initial=self.instance.get_channel_data(
                    channel.content_type.model)
                if self.instance
                else {},
            )
            for channel in channels
        }

    def is_valid(self):
        if is_valid := super().is_valid():
            for channel in self.cleaned_data["channels"]:
                is_valid = is_valid and self.channel_forms[channel].is_valid()
                if not self.channel_forms[channel].is_valid():
                    self.active_channel_tab = channel.pk
        return is_valid

    def save(self, commit=True):
        contact = super().save(commit=False)
        contact.channel_data = {}
        for channel in self.cleaned_data["channels"]:
            form = self.channel_forms[channel]
            contact.set_channel_data(
                channel.content_type.model, form.cleaned_data)
        if commit:
            import_string(settings.CONTACT_STORAGE).save_contact(
                self.environment, contact
            )
        return contact
