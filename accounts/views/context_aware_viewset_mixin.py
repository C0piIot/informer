from django.shortcuts import get_object_or_404
from accounts.models import Environment


class ContextAwareViewSetMixin(object):
    def initial(self, request, *args, **kwargs):
        self.current_environment = get_object_or_404(
            Environment, slug=kwargs.pop("environment"), site=self.request.site
        )
        super().initial(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"environment": self.current_environment})
        return context
