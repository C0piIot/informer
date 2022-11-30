from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, mixins
from contacts.models import Contact
from accounts.rest_permissions import HasEnvironmentPermission
from accounts.views import ContextAwareViewSetMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string
from django.conf import settings
from rest_framework.reverse import reverse
from contacts.rest_permissions import HasContactPermission

contact_storage = import_string(settings.CONTACT_STORAGE)

class ContactSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(
            'contact-detail', 
            kwargs={'environment': self.context['environment'].slug, 'pk': obj.key },
            request=self.context['request']
        )

    
    def validate_channel_data(self, value):
        if not value:
            return {}
        if type(value) != dict:
            raise serializers.ValidationError(_('Channel data is expected to be a dict'))

        errors = dict()
        for channel in self.context['environment'].site.channels.all():
            channel_type = channel.content_type.model
            if channel_type in value:
                channel_serializer = import_string(channel.get_typed_instance().CONTACT_SERIALIZER)(data=value[channel_type])
                if not channel_serializer.is_valid():
                    errors[channel_type] = channel_serializer.errors
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return value


    def create(self, validated_data):
        validated_data = {k: v for k, v in validated_data.items() if v is not None }
        contact = Contact(**validated_data)
        contact_storage.save_contact(self.context['environment'], contact)
        return contact

    def update(self, contact, validated_data):
        validated_data = {k: v for k, v in validated_data.items() if v is not None }
        for attr, value in validated_data.items():
            setattr(contact, attr, value)
        contact_storage.save_contact(self.context['environment'], contact)
        return contact

    class Meta:
        model = Contact
        fields = ['url', 'key', 'public_key', 'name', 'contact_data', 'channel_data']


class ContactViewSet(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    ContextAwareViewSetMixin,
    GenericViewSet):
    serializer_class = ContactSerializer
    permission_classes = [HasContactPermission]
    queryset = Contact.objects.none()

    def get_object(self):
        contact = contact_storage.get_contact(self.current_environment, self.kwargs['pk'])
        self.check_object_permissions(self.request, contact)
        return contact


    def perform_destroy(self, instance):
        instance.delete() #TODO

    