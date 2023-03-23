from django.conf import settings


def rollbar_settings(request):

    return {
        "ROLLBAR_CLIENT_TOKEN": settings.ROLLBAR_CLIENT_TOKEN,
        "ROLLBAR_ENVIRONMENT": settings.ROLLBAR["environment"],
        "ROLLBAR_CODE_VERSION": settings.BUILD_VERSION.split('.')[-1] #Last element is the commit sha1
    }


def build_version(request):
    return {
        "BUILD_VERSION" : settings.BUILD_VERSION
    }