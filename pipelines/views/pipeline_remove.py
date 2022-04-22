from django.urls import reverse
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from .pipeline_filtered_mixin import PipelineFilteredMixin

class PipelineRemove(PipelineFilteredMixin, DeleteView):

    def get(self, request):
         return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        self.object.environments.remove(self.current_environment)
        messages.success(self.request, "%s was removed successfully" % self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('pipelines:home', kwargs={'environment': self.current_environment.slug })
