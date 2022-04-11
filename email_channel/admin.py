from django.contrib import admin

from .models import EmailChannel

@admin.register(EmailChannel)
class EmailChannelAdmin(admin.ModelAdmin):
	pass
