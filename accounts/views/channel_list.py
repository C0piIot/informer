from .channel_list_mixin import ChannelListMixin
from django.views.generic.base import TemplateView

class ChannelList(ChannelListMixin, TemplateView):
    pass
