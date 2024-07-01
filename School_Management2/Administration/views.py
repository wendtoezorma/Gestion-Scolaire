from .decorators import admin_required, student_required

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import Administration
from .forms import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm

from django.contrib.auth.models import User

from django.http import HttpResponseForbidden

# Create your views here.
def index(request):
    return render(request,"Administration/index.html")


def connexion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #nom = form.cleaned_data.get('nom')
            email = form.cleaned_data.get('email')
            mot_de_passe = form.cleaned_data.get('mot_de_passe')
            try:
                user = Administration.objects.get(email=email) 
                if mot_de_passe == user.mot_de_passe:
                    #auth_login(request, user)
                    return redirect('admin_dashboard')  # Rediriger vers une page d'accueil ou tableau de bord
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Administration.DoesNotExist:
                messages.error(request, "Adresse email non trouvée.")
        else:
            messages.error(request, "Veuillez vérifier les informations saisies.")
    else:
        form = LoginForm()
    return render(request, "Administration/connexion.html", {'form': form})

######################## MOT DE PASSE OUBLIE  ######################

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from GestionScolaire.settings import EMAIL_HOST_USER

def forgot_password(request):
    if request.method=='POST':
        email= request.POST.get("email")
        #La ligne suivante verifie si l'email existe dans la base de donnée, plus précisement dans la table Administration
        user = Administration.objects.filter(email=email).first()
        
        """subject='Mot de passe oublié'
        message = f"Mr/Mme.{user.nom}  merci pour votre boulot"
    
        recipient_list = [email]
        send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)"""
         
        
        '''if user:
            print("send email")
            msg=EmailMessage(
                "Test send email django",
                "Bonjour juste un test",
                ######## EMETEUR ########
                "gedeonouedraogo15@gmail.com",
                ######### Recepteur #######
                [user.email]
            )
            
        else:
            print("user does not exist")'''
    return render(request,"Administration/forgot_password.html", {})

######################## MOT DE PASSE OUBLIE  ######################

def update_password(request):
    return render(request,"Administration/update_password.html")



# la page ou il y aura tous les elements concernant l'admin
#@admin_required 
@login_required(login_url='connexion')
def admin_dashboard (request):
    return render(request,"Administration/admin_dashboard.html")


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Etudiant
from .forms import EtudiantCreationForm, EtudiantLoginForm, UpdatePasswordForm
from .paswords_generators import generateur_mdp
@admin_required
def inscription_etudiant(request):
    if request.method == 'POST':
        form = EtudiantCreationForm(request.POST)
        if form.is_valid():
            etudiant = form.save(commit=False)
            #mot_de_passe = form.cleaned_data['mot_de_passe']
            etudiant.mdp_etudiant = generateur_mdp()
            etudiant.save()
            # Envoyer un email à l'étudiant avec le mot de passe généré (optionnel)
            # send_mail(
            #     'Votre mot de passe temporaire',
            #     f'Votre mot de passe temporaire est {mot_de_passe}',
            #     'admin@exemple.com',
            #     [etudiant.email_etudiant],
            #     fail_silently=False,
            # )
            return redirect('admin_dashboard')
    else:
        form = EtudiantCreationForm()
    return render(request, "Administration/insrciption_etudiant.html", {'form': form})

def etudiant_login(request):
    if request.method == 'POST':
        form = EtudiantLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                etudiant = Etudiant.objects.get(email_etudiant=email)
                if check_password(mot_de_passe, etudiant.mdp_etudiant):
                    if not etudiant.password_updated:
                        return redirect('update_password', etudiant_id=etudiant.matricule)
                    # Authentifier l'étudiant et créer une session
                    request.session['etudiant_id'] = etudiant.matricule
                    return redirect('student_dashboard')
                else:
                    form.add_error('mot_de_passe', 'Mot de passe incorrect')
            except Etudiant.DoesNotExist:
                form.add_error('email', 'Email non trouvé')
    else:
        form = EtudiantLoginForm()
    return render(request, 'Administration/etudiant_login.html', {'form': form})

@login_required
def update_password(request, etudiant_id):
    try:
        etudiant = Etudiant.objects.get(matricule=etudiant_id)
    except Etudiant.DoesNotExist:
        return redirect('etudiant_login')

    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            nouveau_mot_de_passe = form.cleaned_data['nouveau_mot_de_passe']
            etudiant.mdp_etudiant = make_password(nouveau_mot_de_passe)
            etudiant.password_updated = True
            etudiant.save()
            # Authentifier l'étudiant et créer une session
            request.session['etudiant_id'] = etudiant.matricule
            return redirect('student_dashboard')#admin_dashboard
    else:
        form = UpdatePasswordForm()
    return render(request, 'Administration\changer_mot_de_passe_etudiant.html', {'form': form})

@login_required
def student_dashboard(request):

    return render(request, 'Administration\student_dashboard.html')
    

#vue pour l'enregistrement d'un cours

#creer une filiere 
@admin_required
def creer_filiere(request):
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Rediriger vers le tableau de bord administrateur
    else:
        form = FiliereForm()
    return render(request, 'Administration/creer_filiere.html', {'form': form})

@admin_required
def creer_cours(request): 


    #if not request.user.is_admin:
        #return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    
    if request.method == 'POST':
        form = CoursModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Rediriger vers le tableau de bord administrateur
    else:
        form = CoursModuleForm()
    return render(request, 'Administration/creer_cours.html', {'form': form})




# vue pur creer un prof 
@admin_required
def creer_professeur(request):
    if request.method == 'POST':
        form = ProfesseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Rediriger vers la liste des professeurs après la création réussie
    else:
        form = ProfesseurForm()
    return render(request, 'Administration/creer_professeur.html', {'form': form})


#cajouter des notes

@admin_required
def creer_note(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_notes')  # Rediriger vers la liste des notes après la création réussie
    else:
        form = NotesForm()
    return render(request, 'Administration/add_note.html', {'form': form})

#enregistrer une classe 
@admin_required
def liste_etudiants_par_classe(request, filiere_id, niveau):
    etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
    context = {
        'etudiants': etudiants,
        'filiere_id': filiere_id,
        'niveau': niveau,
    }
    return render(request, 'Administration/classe.html', context)



@admin_required
#selectionner le niveau et la filiere 
def tri_pour_classe(request):
    filieres = Filiere.objects.all()
    niveaux = Etudiant.objects.values_list('niveau_etudiant', flat=True).distinct()
    return render(request, 'Administration/tri_pour_classe.html', {'filieres': filieres, 'niveaux': niveaux})