from rest_framework.authentication import get_authorization_header

from accounts.rest_permissions import HasEnvironmentPermission


class HasContactPermission(HasEnvironmentPermission):
    keyword = "Bearer"
    has_environment_permission = HasEnvironmentPermission()

    def has_permission(self, request, view):
        if view.action in ["retrieve", "update", "partial_update", "destroy"]:
            return True
        else:
            return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if super().has_permission(request, view):
            return True

        auth = get_authorization_header(request).split()

        if not auth or len(auth) != 2:
            return False

        if auth[0].lower() != self.keyword.lower().encode():
            return False

        return auth[1] == obj.auth_key.encode()
