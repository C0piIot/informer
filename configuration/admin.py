from django.contrib import admin

from .models import Channel, Environment

@admin.register(Environment)
class EnvironmentAdmin(admin.ModelAdmin):
	pass
