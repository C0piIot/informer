from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site

class CurrentSiteMixin(LoginRequiredMixin):
	current_site = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.request.site = get_current_site(request)
		#TODO: check user.site

		#request.user.account if request.user.is_authenticated else None
