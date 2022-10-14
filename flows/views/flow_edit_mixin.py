from flows.forms import step_form_classes
from accounts.views import CurrentEnvironmentMixin
from django.contrib.contenttypes.models import ContentType
from flows.models import Flow
from flows.forms import FlowForm
from django.shortcuts import get_object_or_404
from django.urls import reverse

class FlowEditMixin(CurrentEnvironmentMixin):

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        content_types = ContentType.objects.get_for_models(*step_form_classes.keys())

        flow = get_object_or_404(Flow, environments=self.current_environment, id=self.kwargs['id'])

        context_data.update({
            'flow' : flow,
            'flow_form' : FlowForm(instance=flow),
            'step_types': content_types.values(),
            'new_step_forms': { content_types[model].model : form_class() for model, form_class in step_form_classes.items() },
            'step_forms': { 
                step.order: step_form_classes[type(step.get_typed_instance())](instance=step.get_typed_instance(), auto_id='id_%%s_%d' % step.pk) 
                    for step in flow.steps.all()
            },
            'api_endpoint' : self.request.build_absolute_uri(reverse('flowrun-list', kwargs={'environment': self.current_environment.slug }))
        })
    
        return context_data