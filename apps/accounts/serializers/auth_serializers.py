"""
auth_serializers.py
-------------------
Gère la validation et la transformation des données d'authentification.
"""

from rest_framework import serializers
from ..models import User,validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,TokenError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True, required= False)
    
    class Meta:
        model = User
        fields = ('email','public_id','username','role','password')
        read_only_fields = ('public_id',)
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        request = self.context.get('request')
        if not password :
            raise serializers.ValidationError(" mot de passe est requis.")
        if not email :
         raise serializers.ValidationError("Email est  requis.")
        user = authenticate(email=email, password=password)
        if not user:
            #le user n'a pas ete trouver
            raise serializers.ValidationError("mot de passe ou email")
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est desactivé.")
        #si tout est bon  Génération du token JWT
        refresh = RefreshToken.for_user(user)
        #ajout du binding
        if not request:
            raise serializers.ValidationError("pas de context")
        ip = request.META.get('REMOTE_ADDR')   
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown') 
        refresh["ip"] = ip
        refresh["user_agent"] = user_agent
        refresh.access_token["ip"] = ip
        refresh.access_token["user_agent"] = user_agent        
        (user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'email': user.email,
                'role': user.role,
                'public_id':user.public_id,
            }
        }
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError("mauvais token")        
        
class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")
        try:
            # On crée un RefreshToken à partir du token reçu
            refresh = RefreshToken(refresh_token)

            new_access = refresh.access_token

            data = {
                "access": str(new_access),
                "refresh": str(refresh),
            }

            return data

        except TokenError:
            raise serializers.ValidationError("Refresh token invalide ou expiré.")

 
 
 
        
        
        
        