from django.urls import path
from Administration.views import *
###Pour le mdp oublié
#from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', connexion, name='connexion'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('upload_file', upload_file, name='upload_file'),
    path('display', display_table, name='display'),
    ############################################################################################################
    #1-
    #path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    #path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    #un uid codé en base 64 avec un token
    #path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    #path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
    
    ############################################################################################################
    path("update_password",update_password,name="update_password"),
    path('creer-filiere/', creer_filiere, name='creer_filiere'),
    path('creer-cours/', creer_cours, name='creer_cours'),
    path('Ad', index, name='home'),
    path('inscription_etudiant/',inscription_etudiant,name='inscription_etudiant'),
    #path('etudiant_login', etudiant_login, name= 'etudiant_login')
    path('login/', etudiant_login, name='etudiant_login'),
    path('update-password/<int:etudiant_id>/', update_password, name='update_password'),
    path('creer_professeur/',creer_professeur,name ='creer_professeur'),
    path('creer_note/',creer_note, name = 'creer_note'),
    path('classe/<int:filiere_id>/<str:niveau>/', liste_etudiants_par_classe, name='liste_etudiants_par_classe'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('tri_pour_classe/', tri_pour_classe, name= 'tri_pour_classe' ),
    path("forgot_password", forgot_password,name="forgot_password"),
    path('student_Notes/', student_Notes, name= 'student_Notes'),
    path('select_module/<int:filiere_id>/<str:niveau>/', select_module, name='select_module'),
    path('voir_notes/<int:filiere_id>/<str:niveau>/', voir_notes, name='voir_notes'),
    path('modifier_note/<int:note_id>/', modifier_note, name='modifier_note'),
    path('classe/<int:filiere_id>/<str:niveau>/', liste_etudiants_par_classe, name='liste_etudiants_par_classe'),
    
]

"""
urlpatterns = [
    path('', connexion, name='connexion'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('creer-filiere/', creer_filiere, name='creer_filiere'),
    path('creer-cours/', creer_cours, name='creer_cours'),
    path('Ad', index, name='home'),
    path('inscription_etudiant/',inscription_etudiant,name='inscription_etudiant'),
    #path('etudiant_login', etudiant_login, name= 'etudiant_login')
    path('login/', etudiant_login, name='etudiant_login'),
    path('update-password/<int:etudiant_id>/', update_password, name='update_password'),
    path('creer_professeur/',creer_professeur,name ='creer_professeur'),
    path('creer_note/',creer_note, name = 'creer_note'),
    path('classe/<int:filiere_id>/<str:niveau>/', liste_etudiants_par_classe, name='liste_etudiants_par_classe'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('tri_pour_classe/', tri_pour_classe, name= 'tri_pour_classe' ),
  


"""