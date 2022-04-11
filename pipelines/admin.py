from django.contrib import admin
from .models import *


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
	pass