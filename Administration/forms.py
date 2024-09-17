# forms.py
from .models import *
from django import forms
from django.utils.translation import gettext_lazy as _


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

class EtudiantCreationForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label='Mot de passe temporaire')

    class Meta:
        model = Etudiant
        fields = [
            'nom_etudiant', 'prenom_etudiant', 'photo','email_etudiant', 'telephone_etudiant', 
            'sexe_etudiant', 'Date_naiss_etudiant', 'lieu_naiss_etudiant', 
            'nationalite_etudiant', 'niveau_etudiant', 'annee_academique_etudiant', 
            'filiere', 'mot_de_passe','bourse']
        widgets = {
            #'nom_etudiant' : forms.Input(attrs={"placeholder": "Mot de passe"}),
            'sexe_etudiant': forms.Select(attrs={'class': 'form-control'}),
            'niveau_etudiant': forms.Select(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'annee_academique_etudiant': forms.Select(attrs={'class': 'form-control'}),
            'mot_de_passe': forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
            'mot_de_passe': forms.TextInput(attrs={'class': 'form-control'}),
        }
       


    
class EtudiantLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(), label='Mot de passe')

class UpdatePasswordForm(forms.Form):
    nouveau_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        label='Nouveau mot de passe',
        min_length=8,  # Optionnel : vous pouvez ajouter une validation de longueur minimale
    )
    confirmation_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirmer le nouveau mot de passe',
        min_length=8,  # Optionnel : pour correspondre à la longueur minimale du mot de passe
    )

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
        fields = ['nom_filiere',]
        widgets ={
            'nom_filiere': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfesseurForm(forms.ModelForm):
    class Meta:
        model = professeurs
        fields = '__all__' 
        
        widgets = {
            'niveau_prof': forms.Select(attrs={'class': 'form-control'}),
        }


#debut


#pour la formulaire  du compte admin 

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

#formulire de creation d'un compte adminstration 
# pour le connexion 
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
  
from django import forms
from .models import Administration

# pour lauthentification




#creer son cours
class CoursModuleForm(forms.ModelForm):
    class Meta:
        model = Cours_Module
        fields = ['nom_module', 'credit_module', 'volume_horaire', 'filiere', 'professeur','niveau',]
        widgets ={
            'nom_module': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_module': forms.TextInput(attrs={'class': 'form-control'}),
            'volume_horaire': forms.TextInput(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'professeur': forms.Select(attrs={'class': 'form-control'}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CoursModuleForm, self).__init__(*args, **kwargs)
        self.fields['professeur'].queryset = professeurs.objects.all()
    


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
    class Meta:
        model = UploadedFile
        fields = '__all__'



from django.contrib.auth.models import User 
    
class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Extraire 'request' des kwargs s'il est passé!
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
        fields = ['etudiant', 'tranche_1', 'tranche_2', 'tranche_3','frais_inscription']
        widgets = {
            'etudiant': forms.Select(attrs={'class': 'form-control'}),
            'tranche_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'tranche_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'tranche_3': forms.NumberInput(attrs={'class': 'form-control'}),
            'frais_inscription': forms.NumberInput(attrs={'class': 'form-control'}),
        }

######################### La liste des etudiants pour la scolarité ###################

from .models import Filiere, Etudiant

class FiltreForm(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), required=False, label="Filière")
    niveau = forms.ChoiceField(choices=Etudiant._meta.get_field('niveau_etudiant').choices, required=False, label="Niveau")
    annee_academique = forms.CharField(max_length=100, required=False, label="Année Académique")

###################### POUR LES FICHIERS ########
from django import forms
from .models import CoursFichier

class CoursFichierForm(forms.ModelForm):
    class Meta:
        model = CoursFichier
        fields = ['nom_fichier','fichier', 'type_fichier', 'professeur', 'module', 'filiere', 'niveau', 'annee_academique_cour']
        
        widgets = {
            'professeur': forms.Select(attrs={'class': 'form-fichier'}),
            'type_fichier': forms.Select(attrs={'class': 'form-fichier'}),
            'module': forms.Select(attrs={'class': 'form-fichier'}),
            'filiere': forms.Select(attrs={'class': 'form-fichier'}),
            'niveau': forms.Select(attrs={'class': 'form-fichier'}),
            'annee_academique_cour': forms.Select(attrs={'class': 'form-fichier'}),
        }


####### pour les informations ###########
from .models import Infos
class Infos_Form(forms.ModelForm):
    class Meta:
        model=Infos
        fields=["titre","message","contenu"]
        widgets={
            "titre":forms.TextInput(attrs={"class":"form-control"}),
            "message":forms.TextInput(attrs={"class":"form-control"}),
        }
