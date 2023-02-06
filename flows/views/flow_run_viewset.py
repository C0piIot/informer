from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, mixins
from rest_framework.response import Response
from flows.models import FlowRun, Flow
from django.conf import settings
from django.utils.module_loading import import_string
from accounts.rest_permissions import HasEnvironmentPermission
from accounts.views import ContextAwareViewSetMixin


class FlowTriggerSerializer(serializers.ModelSerializer):
    event = serializers.CharField(write_only=True)
  
    def validate(self, data):
        data['contact'] = import_string(settings.CONTACT_STORAGE).get_contact(self.context['environment'], data['contact_key'])
        if not data['contact']:
            raise serializers.ValidationError({
                'contact_key' : 'There is no contact with the supplied key'
            }, code='invalid_key')
        return data

    def create(self, validated_data):
        flow_runs = []
        flow_run_storage = import_string(settings.FLOW_RUN_STORAGE)
        flow_run_executor = import_string(settings.FLOW_EXECUTOR)
        for flow in Flow.objects.filter(environments=self.context['environment'], trigger=validated_data['event'], enabled=True):
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

    def to_representation(self, instances):
        return { 
            'flow_runs' : [ instance.id for instance in instances ]
        }

    class Meta:
        model = FlowRun
        fields = ['event', 'contact_key', 'event_payload']


class FlowRunViewSet(mixins.CreateModelMixin, ContextAwareViewSetMixin, GenericViewSet):
    serializer_class = FlowTriggerSerializer
    queryset = FlowRun.objects.none()
    permission_classes = [HasEnvironmentPermission]


    
