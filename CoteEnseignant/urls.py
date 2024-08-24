
from django.contrib import admin 
from django.urls import include, path 
from .views import *

urlpatterns = [
    
    path('',connexion_Prof,name='connexion_Prof'),
    path('Professeur_dashboard',Professeur_dashboard, name = "Professeur_dashboard") ,
    path('voir_notes', Voir_notes, name='voir_notes'),
    path('upload_cours_prof', upload_cours_prof , name='upload_cours_prof'),
    path('emploi_du_temps_prof', list_uploaded_files_prof, name='list_uploaded_files_prof'),
    path('classe_pour_prof/<int:filiere_id>/<str:niveau>/<int:professeur_id>', afficher_classe, name='liste_etudiants_par_classe'),
    path('select_module_pour_prof/<int:filiere_id>/<str:niveau>/', select_module_pour_prof, name='select_module_pour_prof'),
    path('cours_list_prof/', cours_list_prof, name='cours_list_prof'),
    path('display_table_prof/<int:file_id>/', display_table_prof, name='display'),
    
]
