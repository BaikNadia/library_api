from rest_framework import permissions

class IsLibrarianOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['librarian', 'admin']

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'

class IsReader(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'reader'

class IsOwnerOrLibrarian(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type in ['librarian', 'admin']:
            return True
        return obj.user == request.user
