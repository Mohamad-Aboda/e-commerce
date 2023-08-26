from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only permissions for all users
        return request.user and request.user.is_staff and request.user.is_superuser  # Allow only admins to create, update, delete
