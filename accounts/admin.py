from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	readonly_fields = ('date_joined',)
	search_fields = ('email__startswith', 'first_name__startswith', 'site__name__startswith',)
	list_filter = ('is_staff',)
	list_select_related = ('site',)
	list_display = ('email', 'first_name', 'site', 'date_joined', 'is_active', 'is_staff',)