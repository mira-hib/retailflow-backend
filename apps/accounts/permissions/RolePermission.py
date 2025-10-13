from rest_framework.permissions import BasePermission, SAFE_METHODS


class RolePermission(BasePermission):
    """
    Gère les permissions sur les utilisateurs selon le rôle :
    - ADMIN : accès total
    - RH_MANAGER : accès total sauf sur les comptes ADMIN et CUSTOMER
    - Autres (STOCK_MANAGER, CASHIER, CUSTOMER) : uniquement leur propre compte
    """

    def has_permission(self, request, view):
        # L'utilisateur doit être authentifié
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user

        #  ADMIN → accès complet
        if user.role == 'ADMIN':
            return True

        #  RH_MANAGER → accès total sauf sur ADMIN et CUSTOMER
        if user.role == 'RH_MANAGER':
            if obj.role in ['ADMIN', 'CUSTOMER']:
                return False
            return True

        #  STOCK_MANAGER, CASHIER, CUSTOMER → accès uniquement à leur compte
        return obj == user
