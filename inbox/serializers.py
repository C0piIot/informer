""" DRF serializers for Inbox API """

from rest_framework import serializers

from inbox.models import InboxEntry


class InboxEntrySerializer(serializers.ModelSerializer):
    """InboxEntry model serialization"""
    class Meta:
        model = InboxEntry
        fields = [
            "key",
            "contact_key",
            "date",
            "title",
            "message",
            "url",
            "image",
            "read",
            "entry_data",
        ]
