from rest_framework.permissions import (BasePermission,
                                        SAFE_METHODS,
                                        IsAuthenticatedOrReadOnly
                                        )

from reviews.models import UserRoles


class IsAdminOrSafeMethod(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True


class IsAdmin(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.auth and request.user.role == UserRoles.ADMIN)
