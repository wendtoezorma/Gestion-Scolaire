# forms.py
from .models import *
from django import forms
from django.utils.translation import gettext_lazy as _

#pour la connexion  du compte admin 
"""
class LoginForm(forms.Form):
    nom = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=300, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Administration
        exclude = ['last_login']
"""

#pour la connexion  du compte admin nouveau
from django import forms
from django.core import validators
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError 
from .models import Administration
from django.utils.translation import gettext as _  # Assurez-vous que cette ligne est en haut du fichier

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
"""
class AdministrationAuthenticationForm(UserCreationForm):
    class Meta:
        model = Administration
        fields = ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Administration
        fields = ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe')


class AdministrationLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), label="Email")
    password = forms.CharField(label="Mot de passe", strip=False, widget=forms.PasswordInput)
"""
"""
class AdministrationAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'autofocus': True, 'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=300,
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'autocomplete': 'current-password', 'class': 'form-control'})
    )

    error_messages = {
        "invalid_login": _(
            "Veuillez entrer un nom, un email et un mot de passe corrects."
        ),
        "inactive": _("Ce compte est inactif."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if username and email and password:
            try:
                user = Administration.objects.get(nom=username, email=email)
            except Administration.DoesNotExist:
                user = None

            if user and user.check_password(password):
                self.user_cache = user
            else:
                raise self.get_invalid_login_error()

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
        )
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from .forms import AdministrationAuthenticationForm
"""

#from django import forms
#from .models import Etudiant

class EtudiantCreationForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label='Mot de passe temporaire')

    class Meta:
        model = Etudiant
        fields = [
            'nom_etudiant', 'prenom_etudiant', 'email_etudiant', 'telephone_etudiant', 
            'sexe_etudiant', 'Date_naiss_etudiant', 'lieu_naiss_etudiant', 
            'nationalite_etudiant', 'niveau_etudiant', 'annee_academique_etudiant', 
            'filiere', 'mot_de_passe'
        ]
    

class EtudiantLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')


class UpdatePasswordForm(forms.Form):
    nouveau_mot_de_passe = forms.CharField(widget=forms.PasswordInput, label='Nouveau mot de passe')
    confirmation_mot_de_passe = forms.CharField(widget=forms.PasswordInput, label='Confirmer le nouveau mot de passe')

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get('nouveau_mot_de_passe')
        confirmation = cleaned_data.get('confirmation_mot_de_passe')

        if mot_de_passe != confirmation:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        return cleaned_data

#creer une filiere 

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere
        fields = ['nom_filiere']

"""#creer son cours
class CoursModuleForm(forms.ModelForm):
    class Meta:
        model = Cours_Module
        fields = ['nom_module', 'credit_module', 'volume_horaire', 'filiere']"""


class ProfesseurForm(forms.ModelForm):
    class Meta:
        model = professeurs
        fields = '__all__'  



#debut


#pour la formulaire  du compte admin 

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

#formulire de creation d'un compte adminstration 
"""
class AdministrationCreationForm(UserCreationForm):
    class Meta:
        model = Administration
        fields = ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe')
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if email and username and password:
            self.user_cache = authenticate(self.request, email=email, password=password, username=username)
            if self.user_cache is None:
                raise forms.ValidationError("Les informations d'identification sont incorrectes.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Ce compte est inactif.")
        return self.cleaned_data
    
    def get_user(self):
        return self.user_cache

    
# Formulaire de modification d'utilisateur personnalisé
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Administration # Spécifie le modèle à utiliser pour ce formulaire
        fields = ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe')

"""
# pour le connexion 
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
  
from django import forms
from .models import Administration

# pour lauthentification
'''
User = get_user_model()
class AdministrationLoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'autofocus': True}))  # Champ pour l'email
    password = forms.CharField(label="Mot de passe", strip=False, widget=forms.PasswordInput)  # Champ pour le mot de passe

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Veuillez entrer une adresse email et un mot de passe valides.")  # Message d'erreur pour une connexion invalide
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Ce compte est inactif.")  # Message d'erreur si le compte est inactif
        return self.cleaned_data

    def get_user(self):
        return self.user_cache  # Retourne l'utilisateur authentifié

'''




#creer son cours
class CoursModuleForm(forms.ModelForm):
    class Meta:
        model = Cours_Module
        fields = ['nom_module', 'credit_module', 'volume_horaire', 'filiere', 'professeur']

    def __init__(self, *args, **kwargs):
        super(CoursModuleForm, self).__init__(*args, **kwargs)
        self.fields['professeur'].queryset = professeurs.objects.all()
    '''class Meta:
        model = Cours_Module
        fields = ['nom_module', 'credit_module', 'volume_horaire', 'filiere']'''


#pour enregistrer des notes

class NotesForm(forms.ModelForm):
    
    class Meta:
        model = Notes
        fields = ['etudiant', 'matiere_module', 'Note1', 'Note2']

    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        self.fields['matiere_module'].widget.attrs['readonly'] = True

        # Remplir le champ 'etudiant' avec les noms et prénoms des étudiants
        self.fields['etudiant'] = forms.ModelChoiceField(
            queryset=Etudiant.objects.all(),
            empty_label=None,  # Ne pas afficher d'option vide
            widget=forms.Select(attrs={'class': 'form-control'})
        )



        
class GenerateTimetableForm(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), required=False)
    enseignant = forms.ModelChoiceField(queryset=professeurs.objects.all(), required=False)
    jour = forms.ChoiceField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')], required=False)
    
    
########################################################################################################

class UploadFileForm(forms.Form):
    file = forms.FileField()


from django.contrib.auth.models import User 
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Extraire 'request' des kwargs s'il est passé
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Utiliser l'email comme identifiant pour l'authentification
            self.user = authenticate(request=self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Email ou mot de passe invalide.')
        else:
            raise forms.ValidationError('Email et mot de passe sont requis.')

        return cleaned_data

    def get_user(self):
        return self.user

#pour l'administration



from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Administration


class AdministrationCreationForm(UserCreationForm):
    class Meta:
        model = Administration
        fields = ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe')
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}),
            
}
class AdministrationAuthenticationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Administration
        fields = ('email', 'password')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Administration
        fields = ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe')
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe'}),
        }
        

from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Administration

class AdministrationAdminForm(forms.ModelForm):
    class Meta:
        model = Administration
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.mot_de_passe:  # Assurez-vous que le mot de passe est fourni
            user.mot_de_passe = make_password(user.mot_de_passe)
        if commit:
            user.save()
        return user


from django import forms
from .models import Scolarite

class ScolariteForm(forms.ModelForm):
    class Meta:
        model = Scolarite
        fields = ['etudiant', 'tranche_1', 'tranche_2', 'tranche_3']
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-control'}),
            'tranche_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'tranche_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'tranche_3': forms.NumberInput(attrs={'class': 'form-control'}),
        }


######################### La liste des etudiants pour la scolarité ###################

from django import forms
from .models import Filiere, Etudiant

class FiltreForm(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), required=False, label="Filière")
    niveau = forms.ChoiceField(choices=Etudiant._meta.get_field('niveau_etudiant').choices, required=False, label="Niveau")
    annee_academique = forms.CharField(max_length=100, required=False, label="Année Académique")

class Scolarite_Form(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['matricule', 'nom_etudiant', 'prenom_etudiant', 'filiere', 'niveau_etudiant', 'annee_academique_etudiant',"montant_total_verse"]