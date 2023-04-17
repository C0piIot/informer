from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import View
from premailer import Premailer

from accounts.mixins import CurrentEnvironmentMixin
from flows.models import Flow


@method_decorator(csrf_exempt, name="dispatch")
class Preview(CurrentEnvironmentMixin, View):
    RENDER_MODE_EMAIL = "email"
    RENDER_MODE_HTML = "html"
    RENDER_MODE_PLAIN = "plain"
    RENDER_MODES = [RENDER_MODE_HTML, RENDER_MODE_PLAIN, RENDER_MODE_EMAIL]
    premailer = Premailer()

    def post(self, request, **kwargs):
        flow = get_object_or_404(
            Flow, environments=self.current_environment, id=self.kwargs["id"]
        )
        message = request.POST.get("message", "").strip()
        render_mode = request.POST.get("mode", self.RENDER_MODE_HTML)
        if render_mode not in self.RENDER_MODES:
            render_mode = self.RENDER_MODE_HTML
        if render_mode == self.RENDER_MODE_PLAIN:
            message = escape(message)
        try:
            response = Template(message).render(
                Context(
                    flow.preview_context,
                    autoescape=render_mode != self.RENDER_MODE_PLAIN,
                )
            )
            if render_mode == self.RENDER_MODE_EMAIL and response:
                response = self.premailer.transform(response)
            return HttpResponse(response)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
