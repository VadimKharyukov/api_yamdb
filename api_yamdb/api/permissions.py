from rest_framework.permissions import (BasePermission,
                                        SAFE_METHODS
                                        )

from reviews.models import UserRoles


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsOwnerOrAdminOrModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            return obj.author == request.user or request.user.role in [
                UserRoles.ADMIN, UserRoles.MODERATOR
                ]
        return False
