from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE methods are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Fundraiser: use owner
        if hasattr(obj, "owner"):
            return obj.owner == request.user

        # Pledge: use supporter
        if hasattr(obj, "supporter"):
            return obj.supporter == request.user

        # If neither field exists, deny access
        return False