from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from flows.models import Flow, FlowStep
from django.db.models import Prefetch

class FlowHistory(LoginRequiredMixin, ListView):
    template_name_suffix = '_history'
    model = Flow
    def get_queryset(self):
        return super().get_queryset().filter(
            id=self.kwargs['id'], site=self.request.site
            ).prefetch_related(
                Prefetch('environments'),
                Prefetch('steps', queryset=FlowStep.objects.select_related(
                    'content_type', 'delay', 'group', 'email', 'push', 'webhook'
                    )
                )
            ).select_related('user')

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data.update({
            'highlight': self.kwargs.get('revision', self.object_list.filter(environments=self.current_environment).first().pk)
        })
        return context_data
