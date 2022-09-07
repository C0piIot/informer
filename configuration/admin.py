from django.contrib import admin

from .models import Account, User

class UserInline(admin.TabularInline):
    model = User
    fields = ('email', 'first_name', 'last_name', 'is_active',)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
	inlines = (UserInline,)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	readonly_fields = ('date_joined',)
	search_fields = ('email__startswith', 'first_name__startswith', 'account__name__startswith',)
	list_filter = ('is_staff',)
	list_select_related = ('account',)
	list_display = ('email', 'first_name', 'account', 'date_joined', 'is_active', 'is_staff',)