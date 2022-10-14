from django.views.generic.base import View
from accounts.views import CurrentAccountMixin
from django.template import Template, Context
from django.http import HttpResponse
from premailer import Premailer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class RenderMail(CurrentAccountMixin, View):
	premailer = Premailer()

	def post(self, request, *args, **kwargs):
		message =request.body.decode('UTF-8').strip()
		return HttpResponse(
			self.premailer.transform(
				Template(message).render(Context())
			) if message else ''
		)
