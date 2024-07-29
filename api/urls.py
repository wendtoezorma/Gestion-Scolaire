from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

#router = DefaultRouter()
#router.register(r'etudiants', EtudiantViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    path('login_Etudiant/', EtudiantLoginView.as_view(), name='etudiant_login'),
    path('etudiant/update_password/<int:etudiant_id>/', UpdatePasswordView.as_view(), name='update_password'),
    path('notes/', EtudiantNotesList.as_view(), name='etudiant_notes_api'),
    path('modules/', ModulesClasseView.as_view(), name='modules_classe_api'),
    path('etudiantprofil/', StudentProfileView.as_view(), name='etudiant_detail'),
]
