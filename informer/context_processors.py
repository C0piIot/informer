from django.conf import settings


def rollbar_settings(request):
    return {
        "ROLLBAR_CLIENT_TOKEN": settings.ROLLBAR_CLIENT_TOKEN,
        "ROLLBAR_ENVIRONMENT": settings.ROLLBAR["environment"],
        "APP_VERSION" : settings.APP_VERSION
    }


def app_version(request):
    return {
        "VERSION" : settings.APP_VERSION
    }