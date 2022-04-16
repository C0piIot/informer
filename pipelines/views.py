from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from configuration.views import CurrentEnvironmentMixin
from .models import Pipeline
from django.db import transaction


class PipelineFilteredMixin(CurrentEnvironmentMixin):
    model = Pipeline

    def get_queryset(self):
        return super().get_queryset().filter(environments=self.current_environment)


class PipelineList(PipelineFilteredMixin, ListView):
    pass
    

class PipelineCreate(CurrentEnvironmentMixin, SuccessMessageMixin, CreateView):
    model = Pipeline
    fields = ('name', 'trigger',)
    template_name_suffix = '_create_form'
    success_message = "%(name)s was created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.environments.add(self.current_environment)
        return response

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'pk': self.object.pk, 'environment': self.current_environment.slug })


class PipelineEdit(PipelineFilteredMixin, SuccessMessageMixin, UpdateView):
    fields = ('name', 'trigger', 'enabled')
    template_name_suffix = '_edit_form'
    success_message = "%(name)s was updated successfully"

    def form_valid(self, form):
        with transaction.atomic():
            self.object.environments.remove(self.current_environment)
            response = super().form_valid(form)
            self.object.environments.add(self.current_environment)
        return response

    def get_success_url(self):
        return reverse('pipelines:edit', kwargs={'pk': self.object.pk, 'environment': self.current_environment.slug })


class PipelineRemove(PipelineFilteredMixin, DeleteView):

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.environments.remove(self.current_environment)
        messages.success(self.request, "%s was removed successfully" % self.object)
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('pipelines:home', kwargs={'environment': self.current_environment.slug })