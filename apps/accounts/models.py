import uuid
import re
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
import re

def validate_password(password:str):
    """
    Vérifie si le mot de passe est fort :
    - au moins 8 caractères
    - contient une majuscule
    - contient une minuscule
    - contient un chiffre
    - contient un caractère spécial
    """
    if len(password)< 8:
        raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")
    if not re.search(r"\d", password):
        raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
    
    return True

# personaliser le manager

class CustomUserManager(BaseUserManager):
    def create_user(self, email : str, password : str =None, role = "CUSTOMER",** extra_fields):
        if not email: 
            raise ValueError("l'email est obligatoire")
        email = self.normalize_email(email)
        
        if role != "CUSTOMER":
            #mot de passe obligatoir si on est pas client 
            if not password : 
                raise ValueError("Un mot de passe est obligatoire pour ce rôle.")
            
            # véfication de la robustesse du mot de passe 
            validate_password(password)
            
        user = self.model(email = email,role = role, **extra_fields)
            
        if password:
            print(password)
            user.set_password(password)
        else:
            #si pas de mot de passe bloquer toute tentative avec un mot de passe 
            raise ValueError("Un mot de passe est obligatoire pour ce rôle.")
            user.set_unusable_password()
        user.save(using = self.db)    
        return user
    
    #creation du super user 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")
        return self.create_user(email, password, **extra_fields)

# modele pour les utilisateur 

class User(AbstractBaseUser, PermissionsMixin):
    
    role_choise = [
        ('ADMIN', 'Administrateur'),
        ('STOCK_MANAGER', 'Gestionnaire_stock'),
        ('RH_MANAGER', 'Gestionnaire_rh'),
        ('CASHIER', 'Caissier'),
        ('CUSTOMER', 'client'),]
    
    #id interne pour les jointure 
    id = models.BigAutoField(primary_key=True)
    
    #id public pour les tokens
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    email = models.EmailField(unique= True)
    
    username = models.CharField(max_length=150)
    
    
    role = models.CharField(max_length=20,choices= role_choise,default= "CUSTOMER")
    
    date_joined = models.DateTimeField(default=timezone.now)
    
    is_active = models.BooleanField(default= True)
    
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    USER_ID_FIELD = 'public_id'
    
    def  __str__(self):
        return f"{self.username} ({self.role})"

    