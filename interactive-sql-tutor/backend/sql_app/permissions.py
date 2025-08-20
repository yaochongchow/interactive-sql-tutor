from rest_framework.permissions import BasePermission

class IsAdminUserOrInstructor(BasePermission):
    """
    Allow authenticated users with Admin or Instructor roles.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) in ["Admin", "Instructor"]
        )