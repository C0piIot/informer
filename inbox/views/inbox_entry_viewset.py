from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, mixins
from inbox.models import InboxEntry
from django.utils.module_loading import import_string
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from accounts.views import ContextAwareViewSetMixin
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.response import Response

inbox_storage = import_string(settings.INBOX_ENTRY_STORAGE)
contact_storage = import_string(settings.CONTACT_STORAGE)

class InboxEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = InboxEntry
        fields = ['key', 'date', 'title', 'message', 'url', 'image', 'read', 'entry_data']


class InboxEntryViewSet(
    mixins.RetrieveModelMixin, 
    mixins.ListModelMixin, 
    ContextAwareViewSetMixin,
    GenericViewSet):
    
    queryset = InboxEntry.objects.none()
    serializer_class = InboxEntrySerializer

    auth_keyword = 'Bearer'

    def perform_authentication(self, request):
        auth =  get_authorization_header(request).split()

        if not auth or len(auth) != 2:
            raise exceptions.AuthenticationFailed(_('Missing auth'))

        if auth[0].lower() != self.auth_keyword.lower().encode():
            raise exceptions.AuthenticationFailed(_('Missing auth'))

        contact_auth = auth[1].decode().split('/')
        
        if not contact_auth or len(contact_auth) != 2:
            raise exceptions.AuthenticationFailed(_('Invalid token'))

        self.contact = contact_storage.get_contact(self.current_environment, contact_auth[0])

        if not self.contact:
            raise exceptions.AuthenticationFailed(_('Invalid token'))

        if contact_auth[1] != self.contact.auth_key:
            raise exceptions.AuthenticationFailed(_('Invalid token'))



    def list(self, request, *args, **kwargs):

        inbox_entries = inbox_storage.get_entries(self.current_environment, self.contact, start_key=None, amount=50)
        #queryset = self.filter_queryset(self.get_queryset())

        #page = self.paginate_queryset(queryset)
        #if page is not None:
        #    serializer = self.get_serializer(page, many=True)
        #    return self.get_paginated_response(serializer.data)

        #serializer = self.get_serializer(queryset, many=True)
        #return Response(serializer.data)
        return Response([])


    def get_object(self):
        inbox_entry = inbox_storage.get_entry(self.current_environment, contact, self.kwargs['pk'])
        self.check_object_permissions(self.request, inbox_entry)
        return inbox_entry