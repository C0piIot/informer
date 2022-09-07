from django.contrib.admin.apps import AdminConfig

class InformerAdminConfig(AdminConfig):
    default_site = 'informer.admin.InformerAdmin'