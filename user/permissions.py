from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticatedOrReadOnly,
)

from user.models import User


class IsTaxAccountantOrAdminOrReadonly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role > User.TAXPAYER:
                return True
            return request.method in SAFE_METHODS
        return False


class IsTaxAccountantOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and request.user.is_authenticated and user.role > User.TAXPAYER
        )


class IsTaxPayer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and request.user.is_authenticated and user.role == User.TAXPAYER
        )


class IsTaxAccountant(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and request.user.is_authenticated and user.role == User.TAXACCOUNTANT
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and request.user.is_authenticated and user.role == User.ADMIN)
