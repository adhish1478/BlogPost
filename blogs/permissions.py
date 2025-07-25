from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    # Custom permission to only allow the author of an object to edit or delete it.

    def has_object_permission(self, request, view, obj):
        # Allow read-only requests (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write/delete only allowed if author
        return obj.author == request.user