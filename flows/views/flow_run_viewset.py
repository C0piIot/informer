from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from accounts.views import CurrentEnvironmentMixin
from rest_framework import serializers, status, mixins
from rest_framework.response import Response
from contacts.forms import ContactKeyField
from flows.models import FlowRun, Flow

class FlowRunSerializer(serializers.ModelSerializer):

    event = serializers.CharField()
    contact = ContactKeyField()
    #event_payload = serializers.JSONField(default=dict, required=False)

    def create(self, validated_data):
        flow_run = FlowRun(
            flow_revision=flow,
            contact_key=validated_data['contact'].key,
            event_payload=validated_data['event_payload'],
        )
        flow_run.contact = validated_data['contact']
        import_string(settings.FLOW_RUN_STORAGE).save_flow_run(environment, flow_run)


    class Meta:
        model = FlowRun
        fields = ['event', 'contact', 'event_payload']


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
    #    FlowRun.dispatch_event(
    #        self.current_environment, 
    #        serializer.validated_data['contact'], 
    #        serializer.validated_data['event'], 
    #        event_payload=serializer.validated_data['payload'] or {})


'''
Flow.objects.filter(environments=environment, trigger=event, enabled=True):
            flow_run = cls(
                flow_revision=flow,
                contact_key=contact.key,
                event_payload=event_payload,
            )
            flow_run.contact = contact
            import_string(settings.FLOW_RUN_STORAGE).save_flow_run(environment, flow_run)
            import_string(settings.FLOW_EXECUTOR).run(flow_run)
'''