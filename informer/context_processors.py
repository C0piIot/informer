from django.conf import settings


def rollbar_settings(request):

    return {
        "ROLLBAR_CLIENT_TOKEN": settings.ROLLBAR_CLIENT_TOKEN,
        "ROLLBAR_ENVIRONMENT": settings.ROLLBAR["environment"],
        "ROLLBAR_CODE_VERSION": settings.GIT_REV
    }


def build_version(request):
    return {
        "BUILD_VERSION": settings.BUILD_VERSION
    }
