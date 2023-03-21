from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from accounts.forms import NewEnvironmentForm
from accounts.models import Channel, Environment

from .mixins import ChannelListMixin


class ChannelList(ChannelListMixin, TemplateView):
    pass


class ChannelCreate(ChannelListMixin, SuccessMessageMixin, CreateView):
    success_url = reverse_lazy("accounts:channel_list")
    success_message = _("Channel was created successfully")
    type = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        try:
            self.type = ContentType.objects.get_by_natural_key(
                "accounts", self.kwargs["type"]
            )
        except (ContentType.DoesNotExist, KeyError) as exc:
            raise Http404 from exc

    def get_form_class(self):
        return import_string(self.type.model_class().CONFIG_FORM)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(site=self.request.site)
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["new_channel_forms"].update(
            {self.type: context_data["form"]})
        return context_data


class ChannelRemove(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("accounts:channel_list")
    success_message = _("Channel was removed successfully")
    model = Channel

    def get_queryset(self):
        return super().get_queryset().filter(site=self.request.site)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)


class ChannelUpdate(ChannelListMixin, SuccessMessageMixin, UpdateView):
    success_url = reverse_lazy("accounts:channel_list")
    success_message = _("Channel was updated successfully")
    model = Channel
    type = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        try:
            self.type = ContentType.objects.get_for_model(
                self.get_object().get_typed_instance()
            )
        except (ContentType.DoesNotExist, KeyError) as exc:
            raise Http404 from exc

    def get_queryset(self):
        return super().get_queryset().filter(site=self.request.site)

    def get_form_class(self):
        return import_string(self.type.model_class().CONFIG_FORM)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = kwargs["instance"].get_typed_instance()
        kwargs.update(site=self.request.site)
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["channel_forms"].update({self.type: context_data["form"]})
        return context_data


class EnvironmentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    success_message = _("Environment %(name)s was created successfully")
    form_class = NewEnvironmentForm
    success_url = reverse_lazy("accounts:environment_list")

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, _("Error creating environment"))
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(site=self.request.site)
        return kwargs


class EnvironmentList(LoginRequiredMixin, ListView):
    model = Environment

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(site=self.request.site)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            new_environment_form=NewEnvironmentForm(site=self.request.site)
        )
        return context_data


class EnvironmentRemove(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Environment
    success_url = reverse_lazy("accounts:environment_list")
    success_message = _("Environment was removed successfully")

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(site=self.request.site)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)
