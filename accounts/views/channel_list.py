from django.views.generic.base import TemplateView

from .channel_list_mixin import ChannelListMixin


class ChannelList(ChannelListMixin, TemplateView):
    pass
