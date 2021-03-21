from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_staff


class ProductReviewPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated and request.method == 'POST':
            return False
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class OrderPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if not request.user.is_authenticated or \
                (request.method in ('POST', 'PUT', 'PATCH') and 'status' in request.data):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
