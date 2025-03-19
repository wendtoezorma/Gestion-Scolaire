from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
# Register your models here.

    
class AdminEtudiant(admin.ModelAdmin):
    list_display=("matricule",'nom_etudiant','prenom_etudiant',"photo","niveau_etudiant","filiere","email_etudiant","bourse","mdp_etudiant",'date_ajout','password_updated','Connecter','type_bac','annee_academique_etudiant',"nom_personne_prevenir","numero_personne_prevenir",'chef_de_classe')

class AdminBoursier(admin.ModelAdmin):
    list_display=('type_bourse',"reduction")

class AdminFiliere(admin.ModelAdmin):
    list_display=('nom_filiere',)

class AdminNote(admin.ModelAdmin):
    list_display=("matiere_module","notes","moyenne","index")
    
class Adminmodule(admin.ModelAdmin):
    list_display=("nom_module","credit_module","volume_horaire","date_ajout",'niveau','professeur', 'filiere' )
    
class AdminProfesseur(admin.ModelAdmin):
    list_display=("nom_prof","prenom_prof","email_prof","niveau_prof","mdp_prof","numero_prof",'date_ajout')
 
class AdminBoursier(admin.ModelAdmin):
    list_display=('type_bourse','reduction')

    
class AdminEnseignement(admin.ModelAdmin) :
    list_display=("professeur",'module_enseigner')

class AdminPROFFILIERE(admin.ModelAdmin) :
    list_display=("professeur",'filiere')
    
class AdminInfos(admin.ModelAdmin) :
    list_display=("titre",'message','contenu')
    
class AdminScolarite(admin.ModelAdmin):
    list_display=("etudiant","tranches","total","montant_total_verse","Montant_restant")

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')  # Champs à afficher dans la liste



# admin.py
from django.contrib import admin
from .models import Tache

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut')  # Affiche ces champs dans la liste des tâches
    list_filter = ('statut',)  # Ajoute un filtre par statut
    search_fields = ('titre',)  # Ajoute un champ de recherche sur le titre
    
    professeur = ('professeur')


class AvancementCoursAdmin(admin.ModelAdmin):
   
    list_display = ('etudiant', 'cours_module', 'volume_horaire_total', 'volume_horaire_realise', 'pourcentage_avancement', 'date_op','volume_horaire_restant','heure_debut','heure_fin','image','image2','image3')
    list_filter = ('etudiant', 'cours_module')
    search_fields = ('etudiant__nom_etudiant', 'cours_module__nom_module')
    ordering = ('-date_op',)
    readonly_fields = ('pourcentage_avancement', 'date_op')

admin.site.register(AvancementCours, AvancementCoursAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Administration


from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin




from django.contrib import admin
from .models import Administration
from .forms import  CustomUserChangeForm
# administration/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Administration
from .forms import AdministrationCreationForm

class AdministrationAdmin(UserAdmin):
    add_form = AdministrationCreationForm
    form = CustomUserChangeForm
    model = Administration
    list_display = ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


class AppelPresenceAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'professeur', 'cours', 'date', 'present', 'heure_debut', 'heure_fin')
    list_filter = ('professeur', 'cours', 'date', 'present')
    search_fields = ('etudiant__nom_etudiant', 'etudiant__prenom_etudiant', 'professeur__nom_prof', 'cours__nom_module')
    list_editable = ('present',)
    date_hierarchy = 'date'

admin.site.register(Appel, AppelPresenceAdmin)

admin.site.register(Administration, AdministrationAdmin)



admin.site.register(UploadedFile,UploadedFileAdmin)
admin.site.register(Etudiant,AdminEtudiant)
#admin.site.register(CoursFichier,AdminCoursFichier)
admin.site.register(Filiere,AdminFiliere)
admin.site.register(Notes,AdminNote)
admin.site.register(Cours_Module,Adminmodule)
admin.site.register(professeurs,AdminProfesseur)
admin.site.register(Enseignement,AdminEnseignement)
admin.site.register(Scolarite,AdminScolarite)
admin.site.register(Infos,AdminInfos)
admin.site.register(Boursier,AdminBoursier)
admin.site.register(ProfesseurFiliere,AdminPROFFILIERE)

