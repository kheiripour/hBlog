from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Authorship permission handle by is_author field in profile to access author api views.
    """

    def has_permission(self, request, view):
        return (
            request.user.profile.is_author if request.user.is_authenticated else False
        )
