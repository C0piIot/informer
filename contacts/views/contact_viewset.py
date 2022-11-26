from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, mixins
from contacts.models import Contact
from accounts.rest_permissions import HasEnvironmentPermission
from accounts.views import ContextAwareViewSetMixin
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string


class ContactSerializer(serializers.ModelSerializer):
    
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
        
        return []

    class Meta:
        model = Contact
        fields = ['key', 'name', 'contact_data', 'channel_data']


class ContactViewSet(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    ContextAwareViewSetMixin,
    GenericViewSet):
    serializer_class = ContactSerializer
    permission_classes = [HasEnvironmentPermission]
    queryset = Contact.objects.none()

    