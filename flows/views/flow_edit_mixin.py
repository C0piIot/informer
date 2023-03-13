from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse

from accounts.views import CurrentEnvironmentMixin
from flows.forms import FlowForm, TestForm, step_form_classes
from flows.models import Flow


class FlowEditMixin(CurrentEnvironmentMixin):
    template_name = "flows/flow_edit_form.html"
    flow = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.flow = get_object_or_404(
            Flow, environments=self.current_environment, id=self.kwargs["id"]
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        content_types = ContentType.objects.get_for_models(
            *step_form_classes.keys())
        context_data.update(
            {
                "flow": self.flow,
                "flow_form": FlowForm(instance=self.flow),
                "test_form": TestForm(
                    flow=self.flow,
                    environment=self.current_environment,
                    initial={"event_payload": self.flow.preview_context},
                ),
                "step_types": content_types.values(),
                "new_step_forms": {
                    content_types[model]: form_class()
                    for model, form_class in step_form_classes.items()
                },
                "step_forms": {
                    step.order: step_form_classes[type(step.get_typed_instance())](
                        instance=step.get_typed_instance(),
                        auto_id="id_%%s_%d" % step.pk,
                    )
                    for step in self.flow.steps.all()
                },
                "url_endpoint": reverse(
                    "flowrun-list",
                    kwargs={"environment": self.current_environment.slug},
                    request=self.request,
                ),
            }
        )

        return context_data
