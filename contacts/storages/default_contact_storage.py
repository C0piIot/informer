from contacts.models import Contact


class DefaultContactStorage:
    @classmethod
    def get_contacts(
            cls, environment, cursor=None, amount=50, filter_key=None,
            filter_name=None):
        queryset = Contact.objects.filter(environment=environment)
        if filter_key:
            queryset = queryset.filter(key=filter_key)
        if filter_name:
            queryset = queryset.filter(name__startswith=filter_name)
        if cursor:
            queryset = queryset.filter(key__gt=cursor)
        contacts = list(queryset[:amount])
        return (contacts, contacts[-1].key if contacts else None)

    @classmethod
    def get_contact(cls, environment, key):
        return Contact.objects.filter(environment=environment, key=key).first()

    @classmethod
    def save_contact(cls, environment, contact):
        contact.environment = environment
        contact.save()

    @classmethod
    def delete_contact(cls, environment, key):
        Contact.objects.filter(environment=environment, key=key).delete()
