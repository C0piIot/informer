from contacts.models import Contact

class DefaultContactStorage:
    @classmethod
    def get_contacts(cls, environment, start_key=None, amount=50, filter_key=None, filter_name=None):
        queryset = Contact.objects.filter(environment=environment)
        if filter_key:
            queryset = queryset.filter(key=filter_key)
        if filter_name:
            queryset = queryset.filter(name__startswith=filter_name)
        if start_key:
            queryset = queryset.filter(key__gt=start_key)
        return queryset[:amount]
        
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