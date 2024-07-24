from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
# Register your models here.

"""class AdminAdministration(admin.ModelAdmin):
    '''list_display=('nom','prenom',"sexe","email","Numero","num_CNIB",'date_ajout')'''
    form = AdministrationAdminForm"""
    
class AdminEtudiant(admin.ModelAdmin):
    list_display=("matricule",'nom_etudiant','prenom_etudiant',"niveau_etudiant","filiere","email_etudiant","bourse","mdp_etudiant",'date_ajout')

class AdminBoursier(admin.ModelAdmin):
    list_display=('type_bourse',"reduction")

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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Administration


from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin




from django.contrib import admin
from .models import Administration
from .forms import AdministrationAuthenticationForm, CustomUserChangeForm
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

admin.site.register(Administration, AdministrationAdmin)




#class AdministrationAdmin(admin.ModelAdmin):
#   form = CustomUserChangeForm
#    add_form = AdministrationAuthenticationForm
#   list_display = ('email', 'nom', 'prenom', 'is_staff', 'is_superuser')
#    search_fields = ('email', 'nom')

#admin.site.register(Administration, AdministrationAdmin)



#admin.site.register(Administration, UserAdmin)



#admin.site.register(Administration,AdminAdministration)
#admin.site.register(Administration, CustomUserAdmin)
#admin.site.register(Administration,AdminAdministration)
admin.site.register(Etudiant,AdminEtudiant)
admin.site.register(Filiere,AdminFiliere)
admin.site.register(Notes,AdminNote)
admin.site.register(Cours_Module,Adminmodule)
admin.site.register(professeurs,AdminProfesseur)
admin.site.register(Enseignement,AdminEnseignement)
admin.site.register(Scolarite,AdminScolarite)
admin.site.register(Boursier,AdminBoursier)

