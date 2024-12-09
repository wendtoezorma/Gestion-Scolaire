from django.urls import path, include
from Administration.views import *
from django.views.generic.base import RedirectView
from django.conf.urls import handler404

handler404 = 'django.views.defaults.page_not_found'

# Pour le mot de passe oublié
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # ======================= SECTION AUTHENTIFICATION =======================
    path('', RedirectView.as_view(url=reverse_lazy('login'), permanent=False), name='home'),  # Redirection vers la page de login
    path('login/', administration_login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # ======================= SECTION SCOLARITÉ =======================
    path('gestion_scolarite/', gestion_scolarite, name='gestion_scolarite'),
    path('get_scolarite/<int:etudiant_id>/', get_scolarite, name='get_scolarite'),
    path('recherche-etudiants/', recherche_etudiants_pour_solarite, name='recherche_etudiants_pour_solarite'),
    path('upload_cours/', upload_cours, name='upload_cours'),
    path('cours_list/', cours_list, name='cours_list'),
    path('obtenir_informations_etudiant', obtenir_informations_etudiant, name='obtenir_informations_etudiant'),

    # ======================= SECTION ADMINISTRATION =======================
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('upload_file', upload_file, name='upload_file'),
    path('display_table/<int:file_id>/', display_table, name='displaytable'),
    path('display_pdf/<int:file_id>/', display_pdf, name='display_pdf'),
    path('files/', list_uploaded_files, name='list_uploaded_files'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),

    # ======================= SECTION PARENTS =======================
    path('parent_connexion/', connexion_personne_prevenir, name='connexion_personne_prevenir'),
    path('parent_dashboard/', dashboard_personne_prevenir, name='dashboard_personne_prevenir'),
    path('parent_deconnexion/', deconnexion_personne_prevenir, name='deconnexion_personne_prevenir'),
    path('personne_prevenir/<str:action_type>/', personne_prevenir_action, name='personne_prevenir_action'),

    # ======================= SECTION ÉTUDIANTS =======================
    path('creer-filiere/', creer_filiere, name='creer_filiere'),
    path('creer-cours/', creer_cours, name='creer_cours'),
    path('inscription_etudiant/', inscription_etudiant, name='inscription_etudiant'),
    path('demander_matricule/', demander_matricule, name='demander_matricule'),
    path('profil_etudiant_cursus/<int:matricule>/', profil_etudiant, name='profil_etudiant_cursus'),
    path('modifier_etudiant/<int:id>/', modifier_etudiant, name='modifier_etudiant'),
    path('loginEtuadiant/', etudiant_login, name='etudiant_login'),
    path('update-password/<int:etudiant_id>/', update_password, name='update_password'),
    path('confirmer_inscription_etudiant/', confirmer_inscription_etudiant, name='confirmer_inscription_etudiant'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('tri_pour_classe/', tri_pour_classe, name='tri_pour_classe'),
    path('student_Notes/', student_Notes, name='student_Notes'),
    path('select_module/<int:filiere_id>/<str:niveau>/', select_module, name='select_module'),
    path('voir_notes/<int:filiere_id>/<str:niveau>/', voir_notes, name='voir_notes'),
    path('modifier_note/<int:note_id>/', modifier_note, name='modifier_note'),
    path('etudiant/<int:matricule>/avancement/', mettre_a_jour_avancement, name='update_avancement'),
    path('etudiant/<int:matricule>/avancement/<int:module_id>/', ajouter_avancement_etape2, name='update_avancement'),
    path('creer_professeur/',creer_professeur,name ='creer_professeur'),
    path('creer_note/',creer_note, name = 'creer_note'),
    path('classe/<int:filiere_id>/<str:niveau>/', liste_etudiants_par_classe, name='liste_etudiants_par_classe'),

    # ======================= SECTION RÉCUPÉRATION DE MOT DE PASSE =======================
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ======================= SECTION RECHERCHE ETUDIANTS =======================
    path('rechercher-etudiants/', rechercher_etudiants, name='rechercher_etudiants'),
    
    # ======================= SECTION API =======================
    path('api/', include('api.urls')),

    # ======================= SECTION ENSEIGNANT =======================
    path('enseignant/', include('CoteEnseignant.urls')),

    # ======================= SECTION PROFESSEURS =======================
    path('prof_dashboard/', prof_dashboard, name='prof_dashboard'),
    path('generer_bulletin/<int:matricule>/<str:semestre>/', generer_bulletin, name='generer_bulletin'),
    path('recherche/', recherche_etudiant, name='recherche_etudiant'),
    path('reinscription/', reinscription_etudiant, name='reinscription_etudiant'),
    path('reinscription/<int:etudiant_id>/', reinscription_etudiant, name='reinscription_etudiant'),
    path('creer-notification/', creer_notification, name='creer_notification'),
    path('notifications/', recuperer_notifications, name='recuperer_notifications'),
    path('notifications_non_lues_count_admin/', notifications_non_lues_count_admin, name='notifications_non_lues_count_admin'),

    # ======================= SECTION INFORMATIONS =======================
    path('infos/', infos, name='infos'),
    path('voir_info/', voir_info, name='voir_infos'),
]

# ======================= SECTION FICHIERS STATIC =======================
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
