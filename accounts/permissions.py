from typing import Type

from requests import Request
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import APIView


class IsAdmin(BasePermission):
    """Allows access only to admin users."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated and request.user.is_admin()


class IsModerator(BasePermission):
    """Allows access to moderators and admins."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated and (request.user.is_admin() or request.user.is_moderator())


class IsOwner(BasePermission):
    """Allow access only if the object is owned by the current user."""

    def has_object_permission(
        self, request: Request, view: APIView, obj: Type[object]
    ) -> bool:
        return obj.user == request.user


class IsAdminOrReadOnly(BasePermission):
    """Allow full access to admin users, read-only access to others."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.method in SAFE_METHODS or (request.user and request.user.is_staff)
        )
