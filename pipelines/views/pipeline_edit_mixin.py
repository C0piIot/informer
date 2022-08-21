from pipelines.forms import step_form_classes
from configuration.views import CurrentEnvironmentMixin
from django.contrib.contenttypes.models import ContentType
from pipelines.models import Pipeline
from pipelines.forms import PipelineForm
from django.shortcuts import get_object_or_404

class PipelineEditMixin(CurrentEnvironmentMixin):

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        content_types = ContentType.objects.get_for_models(*step_form_classes.keys())

        pipeline = get_object_or_404(Pipeline, environments=self.current_environment, id=self.kwargs['id'])

        context_data.update({
            'pipeline' : pipeline,
            'pipeline_form' : PipelineForm(),
            'step_types': content_types.values(),
            'new_step_forms': { content_types[model].model : form_class() for model, form_class in step_form_classes.items() },
            'step_forms': { 
                step.order: step_form_classes[type(step.get_typed_instance())](instance=step.get_typed_instance(), auto_id='id_%%s_%d' % step.pk) 
                    for step in pipeline.steps.all()
            }
        })
    
        return context_data