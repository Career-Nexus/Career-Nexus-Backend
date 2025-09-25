from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied



class IsMentor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.user_type != "mentor":
            raise PermissionDenied("This request is only available to mentors.")
        return True

