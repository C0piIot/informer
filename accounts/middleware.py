from django.http import HttpResponseRedirect


class CheckSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.site_id != request.site.pk:
                return HttpResponseRedirect(f"//{request.user.site.domain}")

        return self.get_response(request)
