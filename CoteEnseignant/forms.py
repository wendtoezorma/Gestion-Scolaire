

from Administration.models import *
from django import forms

class FiltreCoursForm(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), required=False, label="Filière")
    niveau = forms.ChoiceField(choices=Etudiant._meta.get_field('niveau_etudiant').choices, required=False, label="Niveau")
    annee_academique = forms.CharField(max_length=100, required=False, label="Année Académique")
    type_fichier = forms.CharField(max_length=100, required=False, label="Type Fichier")

class ProfesseurLoginForm(forms.Form):
    email_prof = forms.EmailField(label='Email')
    mdp_prof = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email_prof = cleaned_data.get('email_prof')
        mdp_prof = cleaned_data.get('mdp_prof')

        
        if email_prof and mdp_prof:
            try:
                professeur = professeurs.objects.get(email_prof=email_prof)
                if not professeur.check_password(mdp_prof):
                    self.add_error('mdp_prof', 'Mot de passe incorrect')
            except professeurs.DoesNotExist:
                self.add_error('email_prof', 'Email non trouvé')
        return cleaned_data
    


