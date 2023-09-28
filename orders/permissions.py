from rest_framework import permissions

class IsOrderOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the order's user to view their own orders.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET requests for all users.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user making the request is the owner of the order.
        return obj.user == request.user

class IsAuthenticatedOrReadOnlyForPost(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users to create orders for the POST method.
    """

    def has_permission(self, request, view):
        # Allow GET and HEAD requests for all users.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is authenticated for POST requests.
        return request.user.is_authenticated

class ProductListCreateCustomPermission(permissions.BasePermission):
    """
    Custom permission combining multiple permissions.
    """
    
    def has_permission(self, request, view):

        # Check if the user is authenticated for POST requests.
        if request.method == 'POST':
            return IsAuthenticatedOrReadOnlyForPost().has_permission(request, view)
        
        if request.method == 'GET':
            return IsOrderOwnerOrReadOnly().has_permission(request, view)

class ProductRetrieveDestroyPermission(permissions.BasePermission):
    """
    Custom permission combining multiple permissions.
    """
    
    def has_permission(self, request, view):

        # Check if the user is authenticated for POST requests.
        if request.method == 'DELETE' or request.method == 'GET':
            return IsOrderOwnerOrReadOnly().has_permission(request, view)


class ProductItemPermission(permissions.BasePermission):
    """
    Custom permission combining multiple permissions.
    """
    
    def has_permission(self, request, view):

        # Check if the user is authenticated for POST requests.
        if request.method == 'GET' or request.method == 'POST' :
            return IsOrderOwnerOrReadOnly().has_permission(request, view)
        
        if request.method == 'DELETE' or request.method == 'PUT':
            return IsOrderOwnerOrReadOnly().has_permission(request, view)
