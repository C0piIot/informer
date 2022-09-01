from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'login_form' : AuthenticationForm()
        })
        return context_data