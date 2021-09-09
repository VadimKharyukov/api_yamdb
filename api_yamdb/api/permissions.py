from rest_framework import permissions

from reviews.models import UserRoles


class IsAdmin(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.auth and request.user.role == UserRoles.ADMIN)
