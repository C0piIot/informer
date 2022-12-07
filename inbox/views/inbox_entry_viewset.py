from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, mixins
from inbox.models import InboxEntry


class InboxEntryViewSet(
	mixins.RetrieveModelMixin, 
	mixins.ListModelMixin, 
	GenericViewSet):
	 queryset = InboxEntry.objects.none()