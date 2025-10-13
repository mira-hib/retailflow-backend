"""
user_views.py
--------------
Vues REST pour la gestion des utilisateurs.
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.shortcuts import get_object_or_404
from ..models import User
from ..serializers.user_serializers import ChangePasswordSerializer
from ..serializers.user_serializers import PasswordResetConfirmSerializer
from ..serializers.user_serializers import PasswordResetRequestSerializer
from ..serializers.user_serializers import UserUpdateSerializer
from ..permissions.base import IsAdminOrSelf


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data = request.data, context={'request': request})
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)
    
class UserUpdateView(APIView):
    """
    Permet de mettre à jour les informations d’un utilisateur (sauf email et mot de passe).
    Seul l'utilisateur lui-même ou un ADMIN peut modifier.
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def patch(self, request, public_id):
        # 🔹 Récupération de l'utilisateur
        user = get_object_or_404(User, public_id=public_id, is_active=True)
        
        # 🔹 Vérification des permissions
        self.check_object_permissions(request, user)

        # 🔹 Sérialisation et validation
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Utilisateur mis à jour avec succès.",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class UserSoftDeleteView(APIView):
    """
    Effectue une suppression logique d’un utilisateur (soft delete).
    Seul un admin peut désactiver un autre utilisateur.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]

    def delete(self, request, public_id):
        # 🔹 Récupération de l'utilisateur
        user = get_object_or_404(User, public_id=public_id, is_active=True)

        # 🔹 Vérification des permissions
        self.check_object_permissions(request, user)

        # 🔹 Désactivation
        user.is_active = False
        user.save()

        return Response({
            "message": f"L’utilisateur {user.username} a été désactivé avec succès."
        }, status=status.HTTP_200_OK)    
    
    
    