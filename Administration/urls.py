from django.urls import path,include
from Administration.views import *
from django.views.generic.base import RedirectView
###Pour le mdp oublié
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login'), permanent=False), name='home'),  # Redirection de la racine vers la page de login
    path('login/', administration_login_view , name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('gestion_scolarite/', gestion_scolarite, name='gestion_scolarite'),
    path('get_scolarite/<int:etudiant_id>/', get_scolarite, name='get_scolarite'),
    path('recherche-etudiants/', recherche_etudiants_pour_solarite, name='recherche_etudiants_pour_solarite'),
    path('upload_cours/', upload_cours, name='upload_cours'), 
    path('cours_list/', cours_list, name='cours_list'),
    # 
    
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('upload_file', upload_file, name='upload_file'),
    path('display_table/<int:file_id>/', display_table, name='display'),

    path('files/', list_uploaded_files, name='list_uploaded_files'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    ############################################################################################################
    #path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('test-email/', test_email_view, name='test_email'),
    
    ############################################################################################################
     #path("update_password",update_password,name="update_password"),
    path('creer-filiere/', creer_filiere, name='creer_filiere'),
    path('creer-cours/', creer_cours, name='creer_cours'),
    path('inscription_etudiant/',inscription_etudiant,name='inscription_etudiant'),
    path('demander_matricule/', demander_matricule, name='demander_matricule'),
    path('profil_etudiant_cursus/<int:matricule>/', profil_etudiant, name='profil_etudiant_cursus'),
    path('modifier_etudiant/<int:id>/', modifier_etudiant, name='modifier_etudiant'),
    
    #path('etudiant_login', etudiant_login, name= 'etudiant_login')
    path('loginEtuadiant/', etudiant_login, name='etudiant_login'),
    path('update-password/<int:etudiant_id>/', update_password, name='update_password'),
    path('confirmer_inscription_etudiant/', confirmer_inscription_etudiant, name='confirmer_inscription_etudiant'),
    path('creer_professeur/',creer_professeur,name ='creer_professeur'),
    path('creer_note/',creer_note, name = 'creer_note'),
    path('classe/<int:filiere_id>/<str:niveau>/', liste_etudiants_par_classe, name='liste_etudiants_par_classe'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('tri_pour_classe/', tri_pour_classe, name= 'tri_pour_classe' ),
    
    #path("forgot_password", forgot_password,name="forgot_password"),
    path('student_Notes/', student_Notes, name= 'student_Notes'),
    path('select_module/<int:filiere_id>/<str:niveau>/', select_module, name='select_module'),
    path('voir_notes/<int:filiere_id>/<str:niveau>/', voir_notes, name='voir_notes'),
    path('modifier_note/<int:note_id>/', modifier_note, name='modifier_note'),
    path('classe/<int:filiere_id>/<str:niveau>/', liste_etudiants_par_classe, name='liste_etudiants_par_classe'),
    
    #recuperation de mot de passe
    

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('rechercher-etudiants/', rechercher_etudiants, name='rechercher_etudiants'),
    path('api/', include('api.urls')),
    path('enseignant/', include('CoteEnseignant.urls')),
    
    ##################################  Professeurs #####################################
    path('prof_dashboard/', prof_dashboard, name='prof_dashboard'),
    path('generer_bulletin/<int:matricule>/<str:semestre>/', generer_bulletin, name='generer_bulletin'),
    path('recherche/', recherche_etudiant, name='recherche_etudiant'),
    
    ##################################  Informations #####################################
    path('infos/', infos, name='infos'), 
    path('voir_info/', voir_info , name='voir_infos'), 
    
]
########### pour les fichiers #########
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)