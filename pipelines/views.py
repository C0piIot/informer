from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Pipeline

class PipelineList(ListView):
	model = Pipeline

class PipelineCreate(CreateView):
	model = Pipeline