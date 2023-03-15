"""Storing inbox entries"""
from contacts.models import Contact
from inbox.models import Inbox


class DefaultInboxEntryStorage:
    """This storage uses standard django models"""
    @classmethod
    def get_entries(cls, environment, contact, start_key=None, amount=50):
        queryset = Inbox.objects.filter(
            environment=environment, contact=contact)
        if start_key:
            queryset = queryset.filter(key__gt=start_key)
        return queryset[:amount]

    @classmethod
    def get_entry(cls, environment, contact, key):
        return Contact.objects.filter(
            environment=environment, contact=contact, key=key
        ).first()

    @classmethod
    def save_entry(cls, environment, entry):
        entry.environment = environment
        entry.save()
