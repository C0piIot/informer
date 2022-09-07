from django.views.generic.base import TemplateView
from configuration.forms import LoginForm

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'login_form' : LoginForm()
        })
        return context_data