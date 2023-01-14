"""
Permission for admins to add movies
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self,request,view):
        if request.user.is_staff:
            return True
        else:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False


class IsAdmin(permissions.BasePermission):

    def has_permission(self,request,view):
        if request.user.is_staff:
            return True
        else:
            return False
