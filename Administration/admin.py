from django.contrib import admin
from .models import *
# Register your models here.

class AdminAdministration(admin.ModelAdmin):
    list_display=('nom','prenom',"sexe","email","Numero","num_CNIB","mot_de_passe",'date_ajout')
    
class AdminEtudiant(admin.ModelAdmin):
    list_display=("matricule",'nom_etudiant','prenom_etudiant',"email_etudiant","boursier","mdp_etudiant",'date_ajout')

class AdminFiliere(admin.ModelAdmin):
    list_display=('nom_filiere',)

class AdminNote(admin.ModelAdmin):
    list_display=("matiere_module","Note1","Note2","moyenne")
    
class Adminmodule(admin.ModelAdmin):
    list_display=("nom_module","credit_module","volume_horaire","date_ajout")
    
class AdminProfesseur(admin.ModelAdmin):
    list_display=("nom_prof","prenom_prof","email_prof","niveau_prof","mdp_prof","numero_prof",'date_ajout')
    
class AdminEnseignement(admin.ModelAdmin) :
    list_display=("professeur",'module_enseigner')
    
class AdminScolarite(admin.ModelAdmin):
    list_display=("etudiant","tranche_1","tranche_2","tranche_3","total","Montant_restant")
    
    
admin.site.register(Administration,AdminAdministration)
admin.site.register(Etudiant,AdminEtudiant)
admin.site.register(Filiere,AdminFiliere)
admin.site.register(Notes,AdminNote)
admin.site.register(Cours_Module,Adminmodule)
admin.site.register(professeurs,AdminProfesseur)
admin.site.register(Enseignement,AdminEnseignement)
admin.site.register(Scolarite,AdminScolarite)