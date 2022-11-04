from django.contrib.auth.mixins import LoginRequiredMixin
from flows.models import Flow


class FlowFilteredMixin(LoginRequiredMixin):
    model = Flow

    def get_queryset(self):
        return super().get_queryset().filter(environments=self.current_environment)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()

        return queryset.get(id=self.kwargs['id'])
