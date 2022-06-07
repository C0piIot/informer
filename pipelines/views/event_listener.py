from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from configuration.views import CurrentEnvironmentMixin
from rest_framework import serializers, status
from rest_framework.response import Response


class EventSerializer(serializers.Serializer):
    event = serializers.CharField()

class EventListener(GenericViewSet, CurrentEnvironmentMixin):
    serializer_class = EventSerializer

    def dispatch(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        del(kwargs['environment'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.current_account.environments.all()

    @action(methods=['post'], detail=False)
    def event(self, request):
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        



