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
    mot_de_passe = forms.CharField(widget=forms.HiddenInput, label='Mot de passe temporaire',required=False)

    class Meta:
        model = Etudiant
        fields = [
            'nom_etudiant', 'prenom_etudiant', 'photo','email_etudiant', 'telephone_etudiant', 
            'sexe_etudiant', 'Date_naiss_etudiant', 'lieu_naiss_etudiant', 
            'nationalite_etudiant', 'niveau_etudiant', 'annee_academique_etudiant', 
            'filiere','bourse','type_bac','nom_personne_prevenir','numero_personne_prevenir','chef_de_classe',]
        widgets = {
            #'nom_etudiant' : forms.Input(attrs={"placeholder": "Mot de passe"}),
            'sexe_etudiant': forms.Select(attrs={'class': 'form-control'}),
            'niveau_etudiant': forms.Select(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'bourse' :forms.Select(attrs={'class': 'form-control'}),
            'annee_academique_etudiant': forms.Select(attrs={'class': 'form-control' }),
            'mot_de_passe': forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
            'mot_de_passe': forms.TextInput(attrs={'class': 'form-control'}),
            'type_bac': forms.Select(attrs={'class': 'form-control'}),
            #'photo': forms.ClearableFileInput(attrs={'required': False}),
            'photo': forms.HiddenInput(),
            'Date_naiss_etudiant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'jj/MM/AA'}),
            'chef_de_classe' : forms.Select(
            choices=[(True, 'Oui'), (False, 'Non')],
            attrs={'class': 'form-control'},
              # Définir False comme valeur initiale
        )
            
            
        }
        
         
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False
        self.fields['chef_de_classe'].initial = False
        
    
class EtudiantLoginForm(forms.Form):
    #email = forms.EmailField(label='Email')
    matricule = forms.CharField(label='Matricule')
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
        fields = ['nom_filiere','mention']
        widgets ={
            'nom_filiere': forms.TextInput(attrs={'class': 'form-control'}),
            'mention' : forms.Select(attrs={'class': 'form-control'}),
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
from django import forms
from .models import AvancementCours, Cours_Module

class AvancementCoursForm(forms.ModelForm):
    class Meta:
        model = AvancementCours
        fields = ['cours_module', 'volume_horaire_realise','volume_horaire_total']

    # Surcharger le champ pour afficher les cours filtrés dans la vue
    """
    def __init__(self, *args, **kwargs):
        cours_filtrés = kwargs.pop('cours_filtrés', [])
        super().__init__(*args, **kwargs)
        #self.fields['cours_module'].queryset = Cours_Module.objects.filter(id__in=[cours.Id_module for cours in cours_filtrés])
        self.fields['cours_module'].queryset = Cours_Module.objects.filter(Id_module__in=[cours.Id_module for cours in cours_filtrés])

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assurez-vous que 'cours_module' et 'volume_horaire_total' sont bien initialisés
        if 'initial' in kwargs:
            initial_data = kwargs['initial']
            if 'cours_module' not in initial_data:
                initial_data['cours_module'] = kwargs.get('instance', None).cours_module
            if 'volume_horaire_total' not in initial_data:
                initial_data['volume_horaire_total'] = kwargs.get('instance', None).volume_horaire_total

    

        # Placeholder pour description_avancement
        
#creer son cours
class CoursModuleForm(forms.ModelForm):
    class Meta:
        model = Cours_Module
        fields = ['nom_module', 'credit_module', 'volume_horaire', 'filiere', 'professeur','niveau','semestre','unite_enseignement']
        widgets ={
            'nom_module': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_module': forms.TextInput(attrs={'class': 'form-control'}),
            'volume_horaire': forms.TextInput(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'professeur': forms.Select(attrs={'class': 'form-control'}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
            'semestre':forms.Select(attrs={'class': 'form-control'}),
            'unite_enseignement': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CoursModuleForm, self).__init__(*args, **kwargs)
        self.fields['professeur'].queryset = professeurs.objects.all()
    


#pour enregistrer des notes
from django_select2.forms import Select2Widget

class NotesForm(forms.ModelForm):
    
    class Meta:
        model = Notes
        fields = ['id','etudiant', 'matiere_module', 'notes']#, 'Note2'

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
from django_select2.forms import Select2Widget

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
"""
class ScolariteForm(forms.ModelForm):
    class Meta:
        model = Scolarite
        fields = ['etudiant', 'tranche_1', 'tranche_2', 'tranche_3']
        widgets = {
           
            'etudiant': forms.Select(attrs={'class': 'form-control', 'id': 'search-etudiant'}),
            'tranche_1': forms.NumberInput(attrs={'class': 'form-control'}),
            'tranche_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'tranche_3': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ScolariteForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si une instance existe, ne pas rendre les champs en lecture seule
            # mais laisser leurs valeurs par défaut comme celles de la base de données
            

            self.fields['tranche_1'].initial = self.instance.tranche_1
            self.fields['tranche_2'].initial = self.instance.tranche_2
            self.fields['tranche_3'].initial = self.instance.tranche_3
        
        self.fields['etudiant_id'] = forms.CharField(widget=forms.HiddenInput(), required=False)
"""
import json
from django import forms
from .models import Scolarite
from dal import autocomplete
from django_select2.forms import ModelSelect2Widget
from django_select2.forms import Select2TagWidget

class ScolariteForm(forms.ModelForm):
   
    
    class Meta:
        model = Scolarite
        fields = ['etudiant', ]  # Le champ 'tranches' qui sera une liste JSON
        widgets = {
            'etudiant': autocomplete.ModelSelect2(
                url='etudiant-autocomplete',  # Correspond à l'URL de la vue d'autocomplétion
                attrs={
                    'data-placeholder': 'Rechercher un étudiant...',
                    'style': 'width: 100%;',
                }
            )
        }
    #tranches = forms.JSONField(required=False,widget=forms.HiddenInput())  # Ajoutez un champ caché si nécessaire pour gérer les tranches
    """
    def __init__(self, *args, **kwargs):
        super(ScolariteForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            # Si une instance existe, charger les tranches existantes
            tranches = self.instance.tranches  # Obtenez la liste des tranches existantes
            for i in range(3):
                # Créez dynamiquement les champs tranche_1, tranche_2, tranche_3
                self.fields[f'tranche_{i+1}'] = forms.FloatField(
                    initial=tranches[i] if len(tranches) > i else 0,  # Remplir avec les valeurs existantes ou 0
                    required=False,
                    widget=forms.NumberInput(attrs={'class': 'form-control'})
                )

    def clean_tranches(self):
        tranches = []
        for i in range(3):
            tranche_value = self.cleaned_data.get(f"tranche_{i+1}")
            if tranche_value is None:  # Si la valeur est None, on la remplace par 0
                tranche_value = 0
            try:
                tranches.append(float(tranche_value))
            except ValueError:
                raise forms.ValidationError(f"Tranche {i+1} doit être un nombre valide.")
        return tranches
    """
    def __init__(self, *args, **kwargs):
        super(ScolariteForm, self).__init__(*args, **kwargs)
        
        
        # Tranches par défaut (3 tranches)
        for i in range(0):  # 3 tranches par défaut
            self.fields[f'tranche_{i+1}'] = forms.FloatField(
                initial=0,  # Valeur par défaut
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )

    def clean_tranches(self):
        tranches = []
        # Adapté au nombre dynamique de tranches
        max_tranches = len(self.fields)  # Nombre de tranches dans le formulaire
        for i in range(max_tranches):
            tranche_value = self.cleaned_data.get(f"tranche_{i+1}")
            if tranche_value is None:  # Si la valeur est None, on la remplace par 0
                tranche_value = 0
            try:
                tranches.append(float(tranche_value))
            except ValueError:
                raise forms.ValidationError(f"Tranche {i+1} doit être un nombre valide.")
        return tranches
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
        fields = ['nom_fichier', 'fichier', 'type_fichier', 'professeur', 'module', 'filiere', 'niveau', 'annee_academique_cour']
        widgets = {
            'professeur': forms.Select(attrs={'class': 'form-fichier'}),
            #'professeur': forms.Select(attrs={'class': 'form-fichier', 'disabled': 'disabled'}),

            'type_fichier': forms.Select(attrs={'class': 'form-fichier'}),
            'module': forms.Select(attrs={'class': 'form-fichier'}),
            'filiere': forms.Select(attrs={'class': 'form-fichier'}),
            'niveau': forms.Select(attrs={'class': 'form-fichier'}),
            'annee_academique_cour': forms.Select(attrs={'class': 'form-fichier'}),
        }

    def __init__(self, *args, **kwargs):
        professeur_id = kwargs.pop('professeur_id', None)
        super().__init__(*args, **kwargs)

        # Si l'ID du professeur est passé, préremplir le champ 'professeur'
        if professeur_id:
            try:
                professeur = professeurs.objects.get(Id_prof=professeur_id)
                # Préremplir le champ 'professeur' avec l'objet professeur correspondant
                self.fields['professeur'].initial = professeur
                 # Filtrer les modules en fonction du professeur
                modules_professeur = Cours_Module.objects.filter(professeur=professeur)
                self.fields['module'].queryset = modules_professeur
                 # Filtrer les filières en fonction du professeur (en fonction des modules du professeur)
                filieres_professeur = Filiere.objects.filter(cours__professeur=professeur).distinct()
                self.fields['filiere'].queryset = filieres_professeur
            except professeurs.DoesNotExist:
                pass



####### pour les informations ###########
from .models import Infos
class Infos_Form(forms.ModelForm):
    class Meta:
        model=Infos
        fields=["titre","message","contenu"]
        widgets={
            "titre":forms.TextInput(attrs={"class":"form-control"}),
            #"message":forms.TextInput(attrs={"class":"form-control"}),
             
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 12, "style": "width: 100%;"}),  
            "contenu": forms.ClearableFileInput(attrs={"class": "form-control"})
        }

class RechercheEtudiantForm(forms.Form):#pour le bulletin
    matricule = forms.IntegerField(label="Matricule de l'étudiant", widget=forms.TextInput(attrs={
        'placeholder': 'Entrer le matricule de l\'étudiant',
        'class': 'form-control'}))
    semestre = forms.ChoiceField(label="Semestre", choices=[
        ('SEMESTRE 1', 'SEMESTRE 1'),
        ('SEMESTRE 2', 'SEMESTRE 2'),
    ], widget=forms.Select(attrs={
        'class': 'form-control',
    }))