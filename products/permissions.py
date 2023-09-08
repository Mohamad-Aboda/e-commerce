from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_permission(self, request, view):
        # Allow any user, including unauthenticated users, to list products (GET request)
        if request.method == 'GET':
            return True
        # Allow authenticated users to create products (POST request)
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Allow owners to update or delete their products
        return obj.user == request.user
