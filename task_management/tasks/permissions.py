from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
class IsAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Admin').exists()
    
    
class IsUser(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user
    
    