from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.conf import settings
from django.conf.urls.static import static

#router = DefaultRouter()
#router.register(r'etudiants', EtudiantViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('login_Etudiant/', EtudiantLoginView.as_view(), name='etudiant_login'),
    path('etudiant/update_password/<int:etudiant_id>/', UpdatePasswordView.as_view(), name='update_password'),
    path('notes/', EtudiantNotesList.as_view(), name='etudiant_notes_api'),
    path('modules/', ModulesClasseView.as_view(), name='modules_classe_api'),
    
    path('etudiantprofil/', StudentProfileView.as_view(), name='etudiant_detail'),
    path('emploi_du_temps/', UploadedFileListView.as_view(), name='uploaded_file_list_api'),#pour lister les emploi du temps disponible
    path('emploi_du_temps/<int:file_id>/view/', display_table, name='display_table'),#pour voir un emploi du temps
    path('Douwnload_emploi_du_temps/<int:file_id>/download/', download_pdf, name='download_pdf'),#pour le telecharger
    #path('cours-fichiers/', CoursFichierAPI.as_view(), name='cours_fichiers_api'),#envoyer sous un format html
    path('cours-fichiers/', CoursFichierAPI.as_view(), name='cours_fichiers_api'),#envoyer sous un format json 
    path('download-pdf/<int:file_id>/', download_pdf_cours, name='download_pdf'),
    path('scolarite/', ScolariteDetailView.as_view(), name='scolarite-detail'),
    path('infos/', InfosView.as_view(), name='infos_api'),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
