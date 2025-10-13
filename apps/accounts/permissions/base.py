"""
base.py
--------
Contient les classes de permission personnalisées basées sur les rôles.
"""

from rest_framework.permissions import BasePermission

class IsAdminOrSelf(BasePermission):
    """
    Autorise uniquement l'utilisateur lui-même ou un admin.
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and
            (request.user.role == 'ADMIN' or obj == request.user)
        )

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMIN')


class IsStockManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'STOCK_MANAGER')


class IsRHManager(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'RH_MANAGER')


class IsCashier(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'CASHIER')


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'CUSTOMER')
