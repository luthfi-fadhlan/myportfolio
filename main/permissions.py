from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can perform this action."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    - GET/HEAD/OPTIONS: anyone
    - PUT/PATCH: superuser or Editor group
    - POST/DELETE: superuser only
    """
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.method in ("PUT", "PATCH"):
            return request.user.groups.filter(name="Editor").exists()
        return False
