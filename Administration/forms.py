# forms.py
from .models import *
from django import forms

#pour la connexion  du compte admin 
class LoginForm(forms.Form):
    nom = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=300, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Administration
        exclude = ['last_login']


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


#pour enregistrer des notes
"""
class NotesForm(forms.ModelForm):

    class Meta:
        model = Notes
        fields = ['etudiant', 'matiere_module', 'Note1', 'Note2']"""


#debut



#pour la connexion  du compte admin 








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
