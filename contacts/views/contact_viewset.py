from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, mixins
from contacts.models import Contact

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['key', 'name', 'contact_data',]

class ContactViewSet(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.none()
