from rest_framework.permissions import (BasePermission,
                                        SAFE_METHODS,
                                        IsAuthenticatedOrReadOnly
                                        )

from reviews.models import UserRoles


class IsAdmin(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.auth and request.user.role == UserRoles.ADMIN)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return request.user.role == UserRoles.ADMIN
        return False
