from .models import Environment


def environments(request):
    return {'environments': Environment.objects.all() }