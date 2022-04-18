from django.urls import reverse
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from configuration.views import CurrentEnvironmentMixin
from .pipeline_filtered_mixin import PipelineFilteredMixin

class PipelineRemove(PipelineFilteredMixin, DeleteView):

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.environments.remove(self.current_environment)
        messages.success(self.request, "%s was removed successfully" % self.object)
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse('pipelines:home', kwargs={'environment': self.current_environment.slug })
