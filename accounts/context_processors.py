from .models import Account

def account(request):
    return {'account': Account.objects.first() }