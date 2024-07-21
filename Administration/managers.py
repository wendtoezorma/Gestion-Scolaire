# administration/managers.py

from django.contrib.auth.models import BaseUserManager

class AdministrationManager(BaseUserManager):
    def create_superuser(self, email, nom, password=None, **extra_fields):
        """
        Crée et retourne un superutilisateur avec un email, un nom, et un mot de passe.
        """
        if not email:
            raise ValueError('Le superutilisateur doit avoir une adresse email.')
        if not nom:
            raise ValueError('Le superutilisateur doit avoir un nom.')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            **extra_fields
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, email, nom, prenom, numero, date_naissance, num_cnib, sexe, password=None, **extra_fields):
        """
        Crée et retourne un utilisateur normal avec un email, un nom, un prénom, un numéro de téléphone, une date de naissance, un numéro de CNIB, un sexe, et un mot de passe.
        """
        if not email:
            raise ValueError('L\'utilisateur doit avoir une adresse email.')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            numero=numero,
            date_naissance=date_naissance,
            num_cnib=num_cnib,
            sexe=sexe,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
