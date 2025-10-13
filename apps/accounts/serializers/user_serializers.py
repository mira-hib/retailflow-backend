"""
user_serializers.py
-------------------
Sérialise les données liées aux utilisateurs (profil, liste, etc.).
"""


from rest_framework import serializers
from ..models import User,validate_password
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.conf import settings

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la mise à jour partielle des informations utilisateur
    (hors mot de passe et email).
    """
    class Meta:
        model = User
        fields = ['username', 'role', 'is_active']
        read_only_fields = ['is_active', 'role']  # role modifiable seulement par admin

    def update(self, instance, validated_data):
        # Empêche la modification de l’email et du mot de passe
        validated_data.pop('email', None)
        validated_data.pop('password', None)
        return super().update(instance, validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    
    """
    classe du sérializer pour changer de mot de passe
    """
    
    old_password = serializers.CharField(write_only=True)
    
    new_password = serializers.CharField(write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value
    
    def validate_new_password(self,value):
        if not validate_password(value):
            raise serializers.ValidationError("Le nouveau mot de passe n'est pas assez fort.")
        return value
    
    def save(self, **kwargs):
        if not self.context['request'].user:
            raise serializers.ValidationError("pas de user")
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user

signer = TimestampSigner()
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        new_password = data.get("new_password")
        if not new_password:
            raise serializers.ValidationError("il faut definir un mot de passe")
        validate_password(new_password)
        token = data.get("token")
        try:
            public_id = signer.unsign(token, max_age=3600)  # 1h de validité
        except SignatureExpired:
            raise serializers.ValidationError("Le lien de réinitialisation a expiré.")
        except BadSignature:
            raise serializers.ValidationError("Token invalide.")
        
        try:
            user = User.objects.get(public_id=public_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return {"message": "Mot de passe réinitialisé avec succès."}
        
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Aucun utilisateur avec cet email.")
        self.user = user
        return value

    def save(self):
        user = self.user
        token = signer.sign(user.public_id)
        reset_link = f"/reset-password/{token}"
        
        # send_mail(
        #     subject="Réinitialisation de votre mot de passe",
        #     message=f"Voici votre lien pour réinitialiser le mot de passe : {reset_link}",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[user.email],
        # )
        return {"message": f"Email de réinitialisation envoyé. token:{token}"}
