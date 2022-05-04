from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from .current_account_mixin import CurrentAccountMixin
from django.http import HttpResponseRedirect
from pipelines.models import Pipeline
from django.utils.translation import gettext_lazy as _

class ChannelCreate(CurrentAccountMixin, CreateView):
    model = Pipeline
    fields = ('name', 'trigger',)
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('configuration:channel_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.account = self.current_environment.account
        self.object.save()
        messages.success(self.request, _("%(name)s was created successfully") % form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

