from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from configuration.views import CurrentEnvironmentMixin
from rest_framework import serializers, status
from rest_framework.response import Response
from contacts.forms import ContactKeyField
from pipelines.models import PipelineRun, Pipeline

class EventSerializer(serializers.Serializer):

    event = serializers.CharField()
    contact = ContactKeyField()
    payload = serializers.JSONField(default=dict, required=False)


class EventListener(CurrentEnvironmentMixin, GenericViewSet):
    serializer_class = EventSerializer

    def dispatch(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        del(kwargs['environment'])
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({ 'environment': self.current_environment })
        return context

    def get_queryset(self):
        return self.current_account.environments.all()

    @action(methods=['post'], detail=False)
    def event(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        PipelineRun.dispatch_event(
            self.environment, 
            serializer.validated_data['contact'], 
            serializer.validated_data['event'], 
            event_payload=erializer.validated_data['payload'] or {})
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        



