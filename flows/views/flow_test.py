from django.urls import reverse
from flows.views.flow_edit_mixin import FlowEditMixin
from django.views.generic.edit import CreateView
from django.contrib import messages
from accounts.views import CurrentEnvironmentMixin
from django.http import HttpResponseRedirect
from flows.forms import TestForm
from django.utils.translation import gettext_lazy as _

class FlowTest(FlowEditMixin, CurrentEnvironmentMixin, CreateView):
    form_class = TestForm

    def form_valid(self, form):
        #Todo,, y el redirect tiene q ser a otro lao..
        messages.success(self.request, _("%(name)s was created successfully") % form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'test_form' : context_data['form'],
        })
        return context_data


    def get_success_url(self):
        return reverse('flows:run', kwargs={'id': self.object.id, 'environment': self.current_environment.slug })

