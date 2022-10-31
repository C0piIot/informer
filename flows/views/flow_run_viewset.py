from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from accounts.views import CurrentEnvironmentMixin
from rest_framework import serializers, status, mixins
from rest_framework.response import Response
from flows.models import FlowRun, Flow
from django.conf import settings
from django.utils.module_loading import import_string


class FlowRunSerializer(serializers.ModelSerializer):
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
        for flow in Flow.objects.filter(environments=self.context['environment'], trigger=validated_data['event']):
            flow_run = FlowRun(
                flow_revision = flow,
                contact_key = validated_data['contact_key'],
                event_payload = validated_data['event_payload'] or {}
            )
            flow_run.contact = validated_data['contact']
            import_string(settings.FLOW_RUN_STORAGE).save_flow_run(self.context['environment'], flow_run)
            flow_runs.append(flow_run)
        return flow_runs

    class Meta:
        model = FlowRun
        fields = ['event', 'contact_key', 'event_payload']


class FlowRunViewSet(CurrentEnvironmentMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = FlowRunSerializer
    queryset = FlowRun.objects.all()

    def dispatch(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        del(kwargs['environment'])
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({ 'environment': self.current_environment })
        return context

    def get_queryset(self):
        return super().get_queryset().filter(environment=self.current_environment)

    #def perform_create(self, serializer):
        
        