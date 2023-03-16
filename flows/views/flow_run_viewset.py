from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet

from accounts.rest_permissions import HasEnvironmentPermission
from accounts.views import ContextAwareViewSetMixin
from flows.models import Flow, FlowRun


class FlowTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowRun
        fields = ["event", "contact_key", "event_payload"]

    event = serializers.CharField(write_only=True)

    def validate(self, attrs):
        attrs["contact"] = import_string(settings.CONTACT_STORAGE).get_contact(
            self.context["environment"], attrs["contact_key"]
        )
        if not attrs["contact"]:
            raise serializers.ValidationError(
                {"contact_key": "There is no contact with the supplied key"},
                code="invalid_key",
            )
        return attrs

    def create(self, validated_data):
        flow_runs = []
        flow_run_storage = import_string(settings.FLOW_RUN_STORAGE)
        flow_run_executor = import_string(settings.FLOW_EXECUTOR)
        for flow in Flow.objects.filter(
            environments=self.context["environment"],
            trigger=validated_data["event"],
            enabled=True,
        ):
            flow_run = FlowRun(
                flow_revision=flow,
                contact_key=validated_data["contact_key"],
                event_payload=validated_data["event_payload"] or {},
            )
            flow_run.contact = validated_data["contact"]
            flow_run_storage.save_flow_run(
                self.context["environment"], flow_run)
            flow_runs.append(flow_run)
            flow_run_executor.run(flow_run)
        return flow_runs

    def to_representation(self, instance):
        return {"flow_runs": [obj.id for obj in instance]}


class FlowRunViewSet(
        mixins.CreateModelMixin, ContextAwareViewSetMixin, GenericViewSet):
    serializer_class = FlowTriggerSerializer
    queryset = FlowRun.objects.none()
    permission_classes = [HasEnvironmentPermission]
