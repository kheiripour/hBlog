from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.is_author if request.user.is_authenticated else False
    
        
        