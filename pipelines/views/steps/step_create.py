from django.views.generic.edit import CreateView
from configuration.views import CurrentEnvironmentMixin
from django.contrib.messages.views import SuccessMessageMixin
from pipelines.models import Pipeline
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from pipelines.forms import step_form_classes
from django.contrib.contenttypes.models import ContentType


class StepCreate(CurrentEnvironmentMixin, SuccessMessageMixin, CreateView):
    pipeline = None
    success_message = _("Step was edited successfully")

    def get_form_class(self):
        try:
            content_type = ContentType.objects.get_by_natural_key('pipelines', self.kwargs['type'])
            return step_form_classes[content_type.model_class()]
        except (ContentType.DoesNotExist, KeyError):
            raise Http404
        

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
            form.instance.order = self.pipeline.steps.count() + 1
            form.instance.pipeline = self.pipeline
            return super().form_valid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, "Error creating step")

        #self.request.session[form.Meta.model].errors = form.errors
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'id': self.pipeline.id, 'environment': self.current_environment.slug })
