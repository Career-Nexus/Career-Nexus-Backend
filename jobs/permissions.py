from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type != "employer":
            raise PermissionDenied("This request is only available to employers.")
        return True
