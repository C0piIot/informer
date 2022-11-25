from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, mixins
from contacts.models import Contact
from accounts.rest_permissions import HasEnvironmentPermission
from accounts.views import ContextAwareViewSetMixin


class ContactSerializer(serializers.ModelSerializer):
    #email_data = getGenericSerializer(EmailData)()
    #email_data = getGenericSerializer(EmailDa)
    #email_data = https://stackoverflow.com/questions/64810287/django-dynamically-generated-serializer
    #https://stackoverflow.com/questions/30831731/create-a-generic-serializer-with-a-dynamic-model-in-meta

    def create(self, validated_data):
        flow_runs = []
        flow_run_storage = import_string(settings.FLOW_RUN_STORAGE)
        flow_run_executor = import_string(settings.FLOW_EXECUTOR)
        for flow in Flow.objects.filter(environments=self.context['environment'], trigger=validated_data['event']):
            flow_run = FlowRun(
                flow_revision = flow,
                contact_key = validated_data['contact_key'],
                event_payload = validated_data['event_payload'] or {}
            )
            flow_run.contact = validated_data['contact']
            flow_run_storage.save_flow_run(self.context['environment'], flow_run)
            flow_runs.append(flow_run)
            flow_run_executor.run(flow_run)
        return flow_runs

    class Meta:
        model = Contact
        fields = ['key', 'name', 'contact_data', 'email_data']


class ContactViewSet(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
    ContextAwareViewSetMixin):
    serializer_class = ContactSerializer
    permission_classes = [HasEnvironmentPermission]
    queryset = Contact.objects.none()

    