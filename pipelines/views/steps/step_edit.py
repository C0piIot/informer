from django.views.generic.edit import UpdateView
from configuration.views import CurrentEnvironmentMixin
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import PipelineStep, Pipeline
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from pipelines.forms import step_form_classes
from django.contrib.contenttypes.models import ContentType


class StepEdit(CurrentEnvironmentMixin, SuccessMessageMixin, UpdateView):
    pipeline = None
    success_message = _("Step was edited successfully")
    model = PipelineStep

    def get_queryset(self):
        return super().get_queryset().filter(pipeline=self.pipeline)

    def get_form_class(self):
        try:
            content_type = ContentType.objects.get_for_model(self.get_object().get_typed_instance())
            return step_form_classes[content_type.model_class()]
        except (ContentType.DoesNotExist, KeyError):
            raise Http404
    
    def get_object(self):
        return super().get_object().get_typed_instance()      

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pipeline = get_object_or_404(Pipeline, environments=self.current_environment, id=self.kwargs['id'])

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            self.pipeline.environments.remove(self.current_environment)
            self.pipeline.save()
            self.pipeline.environments.add(self.current_environment)
            self.pipeline.steps.filter(order=form.instance.order).delete()
            form.instance.order = self.pipeline.steps.count()
            form.instance.pipeline = self.pipeline
            return super().form_valid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, "Error creating step")

        #self.request.session[form.Meta.model].errors = form.errors
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug })
