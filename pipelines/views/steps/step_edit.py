from django.views.generic.edit import UpdateView
from pipelines.views.pipeline_edit_mixin import PipelineEditMixin
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import PipelineStep, Pipeline
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from pipelines.forms import step_form_classes
from django.contrib.contenttypes.models import ContentType


class StepEdit(PipelineEditMixin, SuccessMessageMixin, UpdateView):
    pipeline = None
    type = None
    success_message = _("Step was edited successfully")
    model = PipelineStep
    template_name = 'pipelines/pipeline_edit_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(pipeline=self.pipeline)

    def get_form_class(self):
        try:
            return step_form_classes[self.type.model_class()]
        except (ContentType.DoesNotExist, KeyError):
            raise Http404
    
    def get_object(self):
        return super().get_object().get_typed_instance()      

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pipeline = get_object_or_404(Pipeline, environments=self.current_environment, id=self.kwargs['id'])
        try:
            self.type = ContentType.objects.get_for_model(self.get_object().get_typed_instance())
        except (ContentType.DoesNotExist, KeyError):
            raise Http404            

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            self.current_environment.pipelines.remove(self.pipeline)
            self.pipeline.user = self.request.user
            self.pipeline.save()
            self.current_environment.pipelines.add(self.pipeline)
            self.pipeline.steps.filter(order=form.instance.order).delete()
            form.instance.pipeline = self.pipeline
            return super().form_valid(form, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['step_forms'][self.object.order] = context_data['form']
        return context_data

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug })
