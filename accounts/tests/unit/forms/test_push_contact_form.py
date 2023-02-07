from django.test import TestCase
from accounts.forms.push_contact_form import (
    TokensWidget,
    MultipleTokensField,
    fcm_token_validation,
)
from django.core.exceptions import ValidationError


class PushContactFormTestCase(TestCase):
    def setUp(self):
        pass

    def testTokensWidget(self):
        tokens_widget = TokensWidget(attrs={"class": "mb-1"})

        self.assertIsNone(tokens_widget.format_value(None))
        self.assertEquals("a\nb\nc", tokens_widget.format_value(["a", "b", "c"]))
        self.assertEquals("abc", tokens_widget.format_value("abc"))

    def testMultipleTokensField(self):
        multiple_tokens_field = MultipleTokensField(
            token_validation=fcm_token_validation
        )

        valid_data = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        self.assertEquals([valid_data], multiple_tokens_field.to_python(valid_data))

        invalid_data = "AA"
        with self.assertRaises(ValidationError):
            multiple_tokens_field.to_python(invalid_data)
