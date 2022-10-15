from django.views.generic.base import View
from accounts.views import CurrentAccountMixin
from django.template import Template, Context
from django.http import JsonResponse
from premailer import Premailer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json


@method_decorator(csrf_exempt, name='dispatch')
class RenderMail(CurrentAccountMixin, View):
	premailer = Premailer()

	def post(self, request, *args, **kwargs):
		html_message = request.POST.get('html_body', '').strip();
		text_message = request.POST.get('text_body', '').strip();
		context = {}
		try:
			context = json.loads(request.POST.get('preview_context', '{}'))
		except json.JSONDecodeError:
			pass
		return JsonResponse({
			'html_preview': self.premailer.transform(
					Template(html_message).render(Context(context))
				) if html_message else '',
			'text_preview': Template(text_message).render(Context(context, autoescape=False))
		})