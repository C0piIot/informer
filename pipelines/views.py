from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Pipeline

class PipelineList(ListView):
	model = Pipeline

class PipelineCreate(SuccessMessageMixin, CreateView):
	model = Pipeline
	fields = ('name', 'trigger',)
	template_name_suffix = '_create_form'
	success_message = "%(name)s was created successfully"

	def get_success_url(self):
		return reverse('pipelines:edit', kwargs={'pk': self.object.pk })


class PipelineEdit(SuccessMessageMixin, UpdateView):
	model = Pipeline
	fields = ('name', 'trigger', 'enabled')
	template_name_suffix = '_edit_form'
	success_message = "%(name)s was updated successfully"

	def get_success_url(self):
		return reverse('pipelines:edit', kwargs={'pk': self.object.pk })

