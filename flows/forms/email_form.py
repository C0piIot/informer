from django.forms import ModelForm

from flows.models import Email


class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = (
            "subject",
            "html_body",
            "text_body",
            "autogenerate_text",
            "from_email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            self.data.get("autogenerate_text")
            if "data" in kwargs
            else self.instance.autogenerate_text
        ):
            self.fields["text_body"].widget.attrs["readonly"] = "readonly"
