from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    message = "Hanya pemilik portofolio dan Editor yang dapat mengubah data."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name="Editor").exists():
            if request.method in ("PUT", "PATCH"):
                return True
            # editor sudah login, jadi beri tahu alasan penolakannya lewat toast
            self.message = "Editor hanya dapat mengubah data, tidak dapat menambah atau menghapusnya."
        return False
