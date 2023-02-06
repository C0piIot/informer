from django.views.generic.edit import CreateView
from flows.views.flow_edit_mixin import FlowEditMixin
from django.contrib.messages.views import SuccessMessageMixin
from flows.models import Flow
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from flows.forms import step_form_classes
from django.contrib.contenttypes.models import ContentType


class StepCreate(FlowEditMixin, SuccessMessageMixin, CreateView):
    type = None
    success_message = _("Step was created successfully")

    def get_form_class(self):
        return step_form_classes[self.type.model_class()]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        try:
            self.type = ContentType.objects.get_for_id(self.kwargs['content_type_id'])
        except ContentType.DoesNotExist:
            raise Http404

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            self.current_environment.flows.remove(self.flow)
            self.flow.user = self.request.user
            self.flow.save()
            self.current_environment.flows.add(self.flow)
            last_step = self.flow.steps.last()
            form.instance.order = last_step.order + 1 if last_step else 1
            form.instance.flow = self.flow
            return super().form_valid(form, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['new_step_forms'].update({ self.type: context_data['form'] })
        return context_data

    def get_success_url(self):
        return reverse('flows:edit', kwargs={'id': self.flow.id, 'environment': self.current_environment.slug })
