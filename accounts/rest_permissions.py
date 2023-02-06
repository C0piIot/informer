from rest_framework import permissions
from rest_framework.authentication import  get_authorization_header

class HasEnvironmentPermission(permissions.BasePermission):

    keyword = 'Bearer'

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return request.user.site_id == request.site.pk
        auth =  get_authorization_header(request).split()

        if not auth or len(auth) != 2:
            return False

        if auth[0].lower() != self.keyword.lower().encode():
            return False

        return auth[1] == view.current_environment.private_key.encode()
