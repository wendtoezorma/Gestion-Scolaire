from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Etudiant 


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Etudiant, Scolarite


import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Etudiant, Scolarite
from django.contrib import messages

from .forms import EtudiantCreationForm, EtudiantLoginForm, UpdatePasswordForm
from .paswords_generators import generateur_mdp
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import Administration
from .forms import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
import pandas as pd
from django.http import HttpResponse
from .models import Emploi
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.shortcuts import render
from .forms import GenerateTimetableForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Etudiant, Notes, Enseignement, Cours_Module
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Etudiant
from .forms import EtudiantCreationForm, EtudiantLoginForm, UpdatePasswordForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from GestionScolaire.settings import EMAIL_HOST_USER
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from django.conf import settings
# Exemple de vue pour envoyer un email de réinitialisation
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.views import View


from django.contrib.auth import authenticate, login  # Importer le login et authenticate
from django.contrib import messages  # Importer messages
################### liste etudiants ####################
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ScolariteForm
from .models import Etudiant, Filiere, Scolarite
from .apperu import apercu_caisse, nombre_etudiants_connecter
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import Http404
from .services import PersonnePrevenir
def administration_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Email ou mot de passe incorrect.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})



def connexion_personne_prevenir(request):
    if request.method == 'POST':
        numero = request.POST.get('numero_personne_prevenir')
        nom = request.POST.get('nom_personne_prevenir')
        try:
            # Vérifier si les informations correspondent à un étudiant
            etudiant = Etudiant.objects.get(
                nom_personne_prevenir=nom,
                numero_personne_prevenir=numero
            )
            # Connecter l'utilisateur si trouvé
            request.session['personne_prevenir_id'] = etudiant.matricule  # Associer l'utilisateur à sa session
            return redirect('dashboard_personne_prevenir')  # Redirection après connexion
        except Etudiant.DoesNotExist:
            return HttpResponse("Nom ou numéro invalide.")
    return render(request, 'parent/connexion_personne_prevenir.html')


def deconnexion_personne_prevenir(request):
    if 'personne_prevenir_id' in request.session:
        del request.session['personne_prevenir_id']
    return redirect('connexion_personne_prevenir')



def dashboard_personne_prevenir(request):
    personne_prevenir_id = request.session.get('personne_prevenir_id')
    if not personne_prevenir_id:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")

    # Récupérer les informations de l'étudiant associé
    try:
        etudiant = Etudiant.objects.get(matricule=personne_prevenir_id)
        return render(request, 'parent/dashboard_personne_prevenir.html', {'etudiant': etudiant})
    except Etudiant.DoesNotExist:
        return HttpResponseForbidden("Aucune donnée trouvée.")



def personne_prevenir_action(request, action_type):
    # Récupérer l'étudiant de la session
    etudiant = PersonnePrevenir.get_etudiant_from_session(request)
   
    
    if not etudiant:
        return redirect('connexion_personne_prevenir')  # Si l'étudiant n'est pas connecté, rediriger vers la page de connexion
   
    # Selon l'action (notes, emploi du temps, fichiers), on appelle la méthode appropriée
    if action_type == 'notes':
        data = PersonnePrevenir.get_notes(etudiant)


        template_name = 'parent/etudiant_notes.html'
    elif action_type == 'emploi_du_temps':
        data = PersonnePrevenir.get_uploaded_files(etudiant)
        template_name = 'parent/uploaded_files.html'
    elif action_type == 'uploaded_files':
        data = PersonnePrevenir.get_uploaded_files()
        template_name = 'parent/uploaded_files.html'
    else:
        raise Http404("Action non valide")

    # Passer les données à un template pour affichage
    return render(request, template_name, {'etudiant': etudiant, 'data': data })

 

class CustomLogoutView(LogoutView):
    template_name = None
    success_url = reverse_lazy('home')

# la page ou il y aura tous les elements concernant l'admin
@login_required(login_url='login')
def admin_dashboard (request):
    
    from.apperu import nombre_etudiants_connecter
    total_etudiants = Etudiant.objects.count()
    etudiant_connecter = nombre_etudiants_connecter()
    total_etudiants_masculin = Etudiant.objects.filter(sexe_etudiant='Masculin').count()
    total_etudiants_feminin = Etudiant.objects.filter(sexe_etudiant='Feminin').count()
    total_professeurs = professeurs.objects.count()
    total_filieres = Filiere.objects.count()
    #total_etudiants_connecter = Etudiant.objects.filter(Connecter=True).count()


    context = {
        'total_etudiants': total_etudiants,
        'total_etudiants_masculin': total_etudiants_masculin,
        'total_etudiants_feminin': total_etudiants_feminin,
        'total_professeurs': total_professeurs,
        'total_filieres': total_filieres,
        'etudiant_connecter':etudiant_connecter,
    }
    return render(request,"Administration/admin_dashboard.html",context)


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits #+ string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
 # Assurez-vous que cette fonction est bien définie
from django.utils import timezone  # Ajoutez ceci pour la gestion des dates

@login_required(login_url='login')
def inscription_etudiant(request):
    if request.method == 'POST':
        form = EtudiantCreationForm(request.POST, request.FILES)
        if form.is_valid():
            etudiant = form.save(commit=False)
            # Générer un mot de passe aléatoire
            raw_password = generate_random_password(8)
            etudiant.mdp_etudiant = make_password(raw_password)  # Hacher le mot de passe
            etudiant_data = form.cleaned_data

            
            
            # Stocker les données dans la session, en convertissant les dates
            request.session['etudiant_data'] = {
                'nom_etudiant': etudiant_data['nom_etudiant'],
                'prenom_etudiant': etudiant_data['prenom_etudiant'],
                'email_etudiant': etudiant_data['email_etudiant'],
                'telephone_etudiant': etudiant_data['telephone_etudiant'],
                'sexe_etudiant': etudiant_data['sexe_etudiant'],
                 #'type_bac':etudiant_data['type_bac'],
                'Date_naiss_etudiant': etudiant_data['Date_naiss_etudiant'].isoformat() if etudiant_data['Date_naiss_etudiant'] else None,
                'lieu_naiss_etudiant': etudiant_data['lieu_naiss_etudiant'],
                'nationalite_etudiant': etudiant_data['nationalite_etudiant'],
                #'filiere': etudiant_data['filiere'],
                'filiere_id': etudiant_data['filiere'].Id_filiere,
                'niveau_etudiant': etudiant_data['niveau_etudiant'],
                'annee_academique_etudiant': etudiant_data['annee_academique_etudiant'],
                'bourse_type': etudiant_data['bourse'].type_bourse,
                'raw_password': raw_password,  # Passer le mot de passe brut à la session
                "numero_personne_prevenir": etudiant_data["numero_personne_prevenir"],
                "nom_personne_prevenir" : etudiant_data["nom_personne_prevenir"],
                'photo_name': request.FILES['photo'].name if 'photo' in request.FILES else None  # Conserver le nom du fichier
                
                 
            }

             # Stocker la photo dans la session sous forme de nom de fichier
            '''photo = request.FILES.get('photo')
            if photo:
                request.session['etudiant_data']['photo_name'] = photo.name  # Conserver le nom de fichier
            '''

            # Afficher la page de récapitulatif
            #etudiant.photo = request.FILES.get('photo')
            return redirect('confirmer_inscription_etudiant')

    else:
        form = EtudiantCreationForm()
    
    return render(request, "Administration/insrciption_etudiant.html", {'form': form})


@login_required(login_url='login')
def modifier_etudiant(request, id):
    etudiant = get_object_or_404(Etudiant, matricule=id)  # Assurez-vous d'utiliser l'attribut approprié ici

    if request.method == 'POST':
        form = EtudiantCreationForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "LES information de l'etudiant ont été modifiées avec succès.")
            return redirect('admin_dashboard')  # Redirige vers le profil après la modification
    else:
        form = EtudiantCreationForm(instance=etudiant)

    return render(request, "Administration/modifier_etudiant.html", {'form': form, 'etudiant': etudiant})



from datetime import datetime

@login_required(login_url='login')
def confirmer_inscription_etudiant(request):
    # Récupérer les données de l'étudiant de la session
    etudiant_data = request.session.get('etudiant_data')
    if etudiant_data:
        # Récupérer la filière à partir de l'ID stocké dans la session
        #filiere = Filiere.objects.get(id=etudiant_data['filiere_id'])
        filiere = Filiere.objects.get(Id_filiere=etudiant_data['filiere_id'])

        etudiant_data['filiere'] = filiere.nom_filiere  # Ajouter le nom de la filière aux données de la session
        # Convertir la date de naissance
        if 'Date_naiss_etudiant' in etudiant_data:
            try:
                date_naissance = datetime.strptime(etudiant_data['Date_naiss_etudiant'], '%Y-%m-%d')
                etudiant_data['date_naissance'] = date_naissance.strftime('%d-%m-%Y')  # Format d'affichage
            except ValueError:
                etudiant_data['date_naissance'] = "Date invalide"

    if request.method == 'POST' and etudiant_data:
        # Convertir la date de naissance de chaîne à objet date
        date_naissance = datetime.strptime(etudiant_data['Date_naiss_etudiant'], '%Y-%m-%d')
        photo = request.FILES.get('photo')  # Si vous utilisez un champ fichier dans le formulaire
        bourse_type = etudiant_data.get('bourse_type')
      
        # Récupérer la filière à partir de l'ID stocké dans la session
        #filiere = Filiere.objects.get(id=etudiant_data['filiere_id'])

        etudiant = Etudiant(
            nom_etudiant=etudiant_data['nom_etudiant'],
            prenom_etudiant=etudiant_data['prenom_etudiant'],
            email_etudiant=etudiant_data['email_etudiant'],
            telephone_etudiant=etudiant_data['telephone_etudiant'],
            sexe_etudiant=etudiant_data['sexe_etudiant'],
            #type_bac=etudiant_data['type_bac'],
            Date_naiss_etudiant=date_naissance,
            lieu_naiss_etudiant=etudiant_data['lieu_naiss_etudiant'],
            nationalite_etudiant=etudiant_data['nationalite_etudiant'],
            #filiere=etudiant_data['filiere'],
            photo= photo,
            filiere=filiere,  # Utiliser l'objet filière récupéré
            bourse=Boursier.objects.get(type_bourse=bourse_type),  # Récupérer l'objet Boursier basé sur le type 
            niveau_etudiant=etudiant_data['niveau_etudiant'],
            annee_academique_etudiant=etudiant_data['annee_academique_etudiant'],
            mdp_etudiant=make_password(etudiant_data['raw_password']) ,# Hacher le mot de passe
            numero_personne_prevenir=etudiant_data["numero_personne_prevenir"],
            nom_personne_prevenir = etudiant_data["nom_personne_prevenir"]

        )
        etudiant.save()  # Enregistrer l'étudiant dans la base de données
           # Ajouter un message de succès
        messages.success(request, "L'inscription de l'étudiant a été confirmée avec succès.")

        # Optionnel: Supprimer les données de la session après l'inscription
        del request.session['etudiant_data']
        return redirect('admin_dashboard')  # Rediriger vers le tableau de bord

    # Gérer le cas où les données ne sont pas disponibles
    if etudiant_data is None:
        return redirect('inscription_etudiant')

    # Si c'est une requête GET, afficher le récapitulatif
    return render(request, 'Administration/recapitulatif_etudiant.html', {
        'etudiant_data': etudiant_data,
        
        
    })



def etudiant_login(request):
    if request.method == 'POST':
        form = EtudiantLoginForm(request.POST)
        if form.is_valid():
            #email = form.cleaned_data['email']
            matricule = form.cleaned_data['matricule']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                #etudiant = Etudiant.objects.get(email_etudiant=email)
                # Rechercher l'étudiant par matricule
                etudiant = Etudiant.objects.get(matricule=matricule)
                if etudiant.check_password(mot_de_passe):
                    if not etudiant.password_updated:

                        # Rediriger vers la mise à jour du mot de passe si ce n'est pas encore fait
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

def update_password(request, etudiant_id):
    try:
        etudiant = Etudiant.objects.get(matricule=etudiant_id)
    except Etudiant.DoesNotExist:
        return redirect('etudiant_login')

    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            nouveau_mot_de_passe = form.cleaned_data['nouveau_mot_de_passe']
            etudiant.set_password(nouveau_mot_de_passe)  # Hash le nouveau mot de passe
            etudiant.password_updated = True# Mettre à jour le champ password_updated
            etudiant.save()
            # Stocker l'identifiant de l'étudiant dans la session
            request.session['etudiant_id'] = etudiant.matricule
            return redirect('student_dashboard')
        else:
            form.add_error(None, "Erreur lors de la mise à jour du mot de passe. Veuillez réessayer.")
    else:
        form = UpdatePasswordForm()
    
    return render(request, 'Administration/changer_mot_de_passe_etudiant.html', {'form': form})



def student_dashboard(request):

    return render(request, 'Administration/student_dashboard.html')
    
@login_required(login_url='login')
def creer_filiere(request):
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Filiere creer avec succes.")
            return redirect('admin_dashboard')  # Rediriger vers le tableau de bord administrateur
    else:
        form = FiliereForm()
    return render(request, 'Administration/creer_filiere.html', {'form': form})

@login_required(login_url='login')
def creer_cours(request): 

    if request.method == 'POST':
        form = CoursModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours creeé avec succes.")
            return redirect('admin_dashboard')  # Rediriger vers le tableau de bord administrateur
    else:
        form = CoursModuleForm()
    return render(request, 'Administration/creer_cours.html', {'form': form})
""""
def mettre_a_jour_avancement(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, pk=etudiant_id)

     # Vérification si l'étudiant est chef de classe
    if not etudiant.chef_de_classe:
        messages.error(request, "Seul un chef de classe peut mettre à jour l'avancement.")
        return redirect('admin_dashboard')  
    cours_filtrés = Cours_Module.objects.filter(filiere=etudiant.filiere, niveau=etudiant.niveau_etudiant)
    avancements = etudiant.avancements.all()
    if request.method == "POST":
        form = AvancementCoursForm(request.POST)
        if form.is_valid():
            avancement = form.save(commit=False)
            avancement.etudiant = etudiant
            avancement.volume_horaire_total = avancement.cours_module.volume_horaire
            avancement.save()
            #etudiant.etat_avancement = True
            etudiant.save()
    else:
        form = AvancementCoursForm()
    return render(request, 'Administration/update_avancement.html', {'form': form, 'etudiant': etudiant,  'cours_filtrés': cours_filtrés, 'avancements': avancements })

"""
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
def select_classe(request):
    filieres = Filiere.objects.all()
    niveaux = Etudiant._meta.get_field('niveau_etudiant').choices  # Récupère les choix définis dans le modèle
    return render(request, 'Administration/select_classe.html', {'filieres': filieres, 'niveaux': niveaux})


def mettre_a_jour_avancement(request, matricule):
    etudiant = get_object_or_404(Etudiant, matricule=matricule)
    
    # Filtrer les modules en fonction du niveau et de la filière de l'étudiant
    modules = Cours_Module.objects.filter(
        niveau=etudiant.niveau_etudiant,
        filiere=etudiant.filiere
    )
    #print(etudiant) 
    #print(modules)
    if request.method == 'POST': 
        # Récupérer les données envoyées par le JavaScript
        try:
            #data = json.loads(request.body)
            #module_id = data.get('cours_module')
            module_id = request.POST.get('cours_module')

            if not module_id:
                return JsonResponse({'error': 'Module non spécifié'}, status=400)
            

            module = get_object_or_404(Cours_Module, pk=module_id)
            
            print(etudiant)
            return JsonResponse({
                'module_id': module.Id_module,
                'nom_module': module.nom_module,
                'volume_horaire': module.volume_horaire,
                'etudiant': etudiant.matricule
            }) 
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données invalides'}, status=400)
        
        
        

    return render(request, 'Administration/update_avancement.html', {'modules': modules, 'etudiant': etudiant})

def ajouter_avancement_etape2(request, matricule, module_id):
    etudiant = get_object_or_404(Etudiant, pk=matricule)
    module = get_object_or_404(Cours_Module, pk=module_id)

     # Récupérer les opérations précédentes de l'étudiant pour ce module
    avancements = AvancementCours.objects.filter(etudiant=etudiant, cours_module=module).order_by('-date_op')

     # Calculer 'horaire_restants' pour chaque avancement
    '''
    for avancement in avancements:
        avancement.horaire_restants = avancement.volume_horaire_restant - avancement.volume_horaire_realise
    '''
    for avancement in avancements:
        if not avancement.volume_horaire_restant or avancement.volume_horaire_restant == 0:
            avancement.volume_horaire_restant = avancement.volume_horaire_total
        avancement.horaire_restants = avancement.volume_horaire_restant - 0#avancement.volume_horaire_realise

    #supprimer apres 
    somme_pourcentage = avancements.aggregate(somme_pourcentage=Sum('pourcentage_avancement'))['somme_pourcentage'] or 0
    

    if request.method == 'POST':
        form = AvancementCoursForm(request.POST)
        if form.is_valid():
            avancement = form.save(commit=False)
            avancement.etudiant = etudiant
            avancement.cours_module = module
            avancement.save()
            return redirect('ajouter_avancement_etape2', matricule=matricule, module_id=module_id)
        else:
                # Afficher les erreurs du formulaire pour le débogage
                print(form.errors)  # Affiche les erreurs dans les logs ou la console
                return render(request, 'Administration/ajouter_avancement.html', {
                    'form': form,
                    'module': module,
                    'etudiant': etudiant,
                    'avancements': avancements
                })
    else:
        form = AvancementCoursForm(initial={
            'cours_module': module,
            'volume_horaire_total': module.volume_horaire
        })

    return render(request, 'Administration/ajouter_avancement.html', {
        'form': form,
        'module': module,
        'etudiant': etudiant,
        'avancements': avancements,
        'somme_pourcentage': somme_pourcentage   # Psupprimer apres
    })
    

def ajouter_avancement_etapeA(request, niveau, filiere, module_id):
    # Récupérer les étudiants de ce niveau et de cette filière
    etudiants = Etudiant.objects.filter(niveau_etudiant=niveau, filiere__Id_filiere=filiere)

    # Récupérer le module correspondant
    module = get_object_or_404(Cours_Module, pk=module_id)
    module_id = request.POST.get('cours_module')

    # Récupérer les avancements pour les étudiants de cette classe
    avancements = AvancementCours.objects.filter(
        etudiant__in=etudiants, cours_module=module
    ).order_by('-date_op')

    # Calculer 'horaire_restants' pour chaque avancement
    for avancement in avancements:
        if not avancement.volume_horaire_restant or avancement.volume_horaire_restant == 0:
            avancement.volume_horaire_restant = avancement.volume_horaire_total
        avancement.horaire_restants = avancement.volume_horaire_restant - 0

    # Supprimer après
    somme_pourcentage = avancements.aggregate(
        somme_pourcentage=Sum('pourcentage_avancement')
    )['somme_pourcentage'] or 0

    if request.method == 'POST':
        form = AvancementCoursForm(request.POST)
        if form.is_valid():
            avancement = form.save(commit=False)
            # Associer un étudiant et un module au nouvel avancement
            etudiant_id = request.POST.get('etudiant')
            etudiant = get_object_or_404(Etudiant, pk=etudiant_id)
            avancement.etudiant = etudiant
            avancement.cours_module = module
            avancement.save()
            return redirect('update_avancement', niveau=niveau, filiere=filiere, module_id=module_id)
        else:
            # Afficher les erreurs du formulaire pour le débogage
            print(form.errors)
            return render(request, 'Administration/ajouter_avancement.html', {
                'form': form,
                'module': module,
                'etudiants': etudiants,
                'avancements': avancements,
                'somme_pourcentage': somme_pourcentage,
            })
    else:
        form = AvancementCoursForm(initial={
            'cours_module': module,
            'volume_horaire_total': module.volume_horaire,
        })

    return render(request, 'Administration/ajouter_avancement.html', {
        'form': form,
        'module': module,
        'etudiants': etudiants,
        'avancements': avancements,
        'somme_pourcentage': somme_pourcentage,  # Supprimer après
    })









from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Etudiant, Cours_Module

def mettre_a_jour_avancementA(request, niveau, filiere):
    # Filtrer les modules en fonction du niveau et de la filière
    modules = Cours_Module.objects.filter(niveau=niveau, filiere=filiere)

    
    if request.method == 'POST':
        try:
            # Récupérer le module sélectionné
            module_id = request.POST.get('cours_module')
            if not module_id:
                return JsonResponse({'error': 'Module non spécifié'}, status=400)

            module = get_object_or_404(Cours_Module, pk=module_id)
            filiere = module.filiere.nom_filiere
            

            # Renvoyer les détails du module et du niveau
            return JsonResponse({
                'module_id': module.Id_module,
                'nom_module': module.nom_module,
                'volume_horaire': module.volume_horaire,
                'niveau': niveau,
                'filiere': filiere,
                
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

    # Rendu du template avec les modules filtrés
    return render(
        request,
        'Administration/update_avancement.html',
        {'modules': modules, 'niveau': niveau, 'filiere': filiere,}
    )




# vue pur creer un prof
@login_required(login_url='login') 
def creer_professeur(request):
    if request.method == 'POST':
        form = ProfesseurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'inscription du proffesseur a été confirmée avec succès.")
            return redirect('admin_dashboard')  # Rediriger vers la liste des professeurs après la création réussie
    else:
        form = ProfesseurForm()
    return render(request, 'Administration/creer_professeur.html', {'form': form})

@login_required(login_url='login')
def liste_etudiants_par_classe(request, filiere_id, niveau):
    etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
    context = {
        'etudiants': etudiants,
        'filiere_id': filiere_id,
        'niveau': niveau,
    }
    return render(request, 'Administration/classe.html', context)


@login_required(login_url='login')
def tri_pour_classe(request):
    filieres = Filiere.objects.all()
    niveaux = Etudiant.objects.values_list('niveau_etudiant', flat=True).distinct()
    return render(request, 'Administration/tri_pour_classe.html', {'filieres': filieres, 'niveaux': niveaux})

@login_required(login_url='login')
def select_module(request, filiere_id, niveau):
    modules = Cours_Module.objects.filter(filiere_id=filiere_id)
    context = {
        'modules': modules,
        'filiere_id': filiere_id,
        'niveau': niveau,
    }
    return render(request, 'Administration/select_module.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notes, Cours_Module, Etudiant
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cours_Module, Notes, Etudiant
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cours_Module, Notes, Etudiant

def creer_note(request):
    if request.method == 'POST':
        etudiants = []
        notes_data = {}

        # Récupérer les matricules des étudiants
        for key in request.POST:
            if key.startswith('etudiant_matricules_'):
                matricule = request.POST.get(key)
                etudiants.append(matricule)

        print("Etudiants récupérés:", etudiants)

        # Récupérer les notes pour chaque étudiant
        for etudiant in etudiants:
            notes_data[etudiant] = []
            for key in request.POST:
                if key.startswith(f'note_{etudiant}_'):
                    note_value = request.POST.get(key)
                    try:
                        notes_data[etudiant].append(float(note_value))
                    except ValueError:
                        print(f"Erreur de conversion pour la note de l'étudiant {etudiant} : {note_value}")
                        pass  # Ignorer si la valeur n'est pas une note valide

        print("Notes Data:", notes_data)

           # Trouver le nombre maximal de notes pour un étudiant
        max_notes_count = max(len(notes) for notes in notes_data.values())

        # Remplir les notes manquantes avec 0
        for etudiant, notes in notes_data.items():
            while len(notes) < max_notes_count:
                notes.append(0)

        # Récupérer l'ID du module
        module_id = request.POST.get('module_id')

        # Traitez les données comme vous le faisiez dans votre code
        etudiants_modifies = []
        try:
            module = Cours_Module.objects.get(Id_module=module_id)
            nom_module = module.nom_module
            professeur = module.professeur
            filiere_id = module.filiere.Id_filiere  # Récupérer l'ID de la filière
            niveau = module.niveau  # Récupérer le niveau
        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('admin_dashboard')

        # Ajouter ou modifier les notes pour chaque étudiant
        for etudiant_matricule, notes in notes_data.items():
            note, created = Notes.objects.get_or_create(
                etudiant_id=etudiant_matricule,
                matiere_module_id=module_id,
                defaults={'notes': notes}
            )

            if not created:
                print(f"Mise à jour des notes pour l'étudiant {etudiant_matricule}")
                note.notes = notes  # Mettre à jour les notes si elles existent déjà
                note.save()

            etudiant = Etudiant.objects.get(pk=etudiant_matricule)
            etudiants_modifies.append(etudiant.nom_etudiant)

        message = (
            f"Des notes ont été ajoutées ou modifiées pour les étudiants suivants dans votre module {nom_module} : "
            f"{', '.join(etudiants_modifies)}."
        )
        creer_notification(
            destinataire_prof=professeur,
            message=message
        )

        messages.success(request, 'Les notes ont été enregistrées avec succès.')
         # Rediriger vers 'liste_etudiants_par_classe' avec les paramètres appropriés
        return redirect(reverse('liste_etudiants_par_classe', kwargs={'filiere_id': filiere_id, 'niveau': niveau}))

        #return redirect('admin_dashboard')

    # Si c'est une requête GET, afficher le formulaire pour ajouter les notes
    if request.method == 'GET':
        module_id = request.GET.get('module_id')
        try:
            module = Cours_Module.objects.get(Id_module=module_id)
            #etudiants = Etudiant.objects.filter(filiere=module.filiere)  # Récupérer les étudiants par filière
            etudiants = Etudiant.objects.filter(
                filiere=module.filiere,
                niveau_etudiant=module.niveau
            )

        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('admin_dashboard')

        context = {
            'module': module,
            'etudiants': etudiants,
            'range_list': range(1, 6)  # Exemple de la gamme de notes
        }
        return render(request, 'Administration/add_note.html', context)

    # Retourner une erreur si la méthode n'est ni GET ni POST
    return redirect('admin_dashboard')


@login_required(login_url='login')
def liste_etudiants_par_classe(request, filiere_id, niveau):
    etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
    modules = Cours_Module.objects.filter(filiere_id=filiere_id)
    filiere = Filiere.objects.get(Id_filiere=filiere_id)  # Récupération de la filière
    
    


    context = {
        'etudiants': etudiants,
        'filiere_id': filiere_id,
        'niveau': niveau,
        'modules': modules,
        'nom_filiere': filiere.nom_filiere,  # Ajout du nom de la filière
        

    }
    return render(request, 'Administration/classe.html', context)


#selectionner le niveau et la filiere 
@login_required(login_url='login')
def tri_pour_classe(request):
    filieres = Filiere.objects.all()
    #niveaux = Etudiant.objects.values_list('niveau_etudiant', flat=True).distinct()
    niveaux = Etudiant._meta.get_field('niveau_etudiant').choices  # Récupère les choix définis dans le modèle
    return render(request, 'Administration/tri_pour_classe.html', {'filieres': filieres, 'niveaux': niveaux})

 

#@login_required
def student_Notes(request):

    # Récupère l'ID de l'étudiant connecté depuis la session
    etudiant_id = request.session.get('etudiant_id')
    
    # Obtient l'objet Etudiant correspondant à l'ID ou renvoie une erreur 404 si non trouvé
    etudiant = get_object_or_404(Etudiant, matricule=etudiant_id)
    
    # Récupère toutes les notes de l'étudiant
    notes = Notes.objects.filter(etudiant=etudiant)
    
    # Si la méthode de la requête est POST (formulaire soumis)
    if request.method == 'POST':
        # Récupère l'ID du module sélectionné dans le formulaire
        module_id = request.POST.get('module_id')
        
        # Vérifie si le module_id est vide
        if not module_id:
            context = {
                'etudiant': etudiant,
                'notes': notes,
                'error': 'Veuillez sélectionner un module.'
            }
            return render(request, 'Administration/student_voir_note.html', context)
        
        # Vérifie si le module_id est valide
        try:
            module_id = int(module_id)
        except ValueError:
            context = {
                'etudiant': etudiant,
                'notes': notes,
                'error': 'Module sélectionné invalide.'
            }
            return render(request, 'Administration/student_voir_note.html', context)
        
        # Obtient l'objet Cours_Module correspondant à l'ID du module
        selected_module = get_object_or_404(Cours_Module, pk=module_id)
        
        # Obtient l'objet Enseignement correspondant au module sélectionné
        enseignement = Enseignement.objects.get(module_enseigner=selected_module)
        
        # Obtient la note de l'étudiant pour le module sélectionné
        note = notes.get(matiere_module=selected_module)
        
        # Prépare le contexte pour le template avec les détails du module sélectionné
        context = {
            'etudiant': etudiant,
            'notes': notes,
            'selected_module': selected_module,
            'enseignement': enseignement,
            'note': note  # Une seule fois suffit
        }
        
        # Rend le template avec le contexte contenant les détails du module sélectionné
        return render(request, 'Administration/student_voir_note.html', context)
    
    # Prépare le contexte pour le template avec les notes de l'étudiant
    context = {
        'etudiant': etudiant,
        'notes': notes
    }
    
    # Rend le template avec le contexte contenant les notes de l'étudiant
    return render(request, 'Administration/student_voir_note.html', context)

@login_required(login_url='login')
def modifier_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    
    if request.method == 'POST':
        notes_str = request.POST.getlist('notes')  # Récupère toutes les notes envoyées
        
        try:
            notes_float = [float(n.replace(',', '.')) for n in notes_str]  # Convertit les valeurs
            note.notes = notes_float  # Met à jour la liste des notes
            note.save()
            messages.success(request, 'Les notes ont été modifiées avec succès.')
            #return redirect('admin_dashboard')
             # Récupérer les informations nécessaires pour la redirection
            filiere_id = note.matiere_module.filiere.Id_filiere  # Supposons que vous avez la filière dans le module
            niveau = note.matiere_module.niveau  # Supposons que vous avez le niveau dans le module

            # Rediriger vers 'liste_etudiants_par_classe' avec les paramètres appropriés
            return redirect(reverse('liste_etudiants_par_classe', kwargs={'filiere_id': filiere_id, 'niveau': niveau}))

        except ValueError:
            messages.error(request, 'Veuillez saisir des nombres valides pour les notes.')
    
    context = {
        'note': note
    }
    return render(request, 'Administration/modifier_note.html', context)


def voir_notes(request, filiere_id, niveau):
    if request.method == 'GET':
        module_id = request.GET.get('module_id')
        filiere_id = int(filiere_id)
       
        
        # Récupérer tous les modules pour cette filière
        modules = Cours_Module.objects.filter(filiere_id=filiere_id, )
        
        
        # Initialiser les variables
        module_selected = None
        notes = None
        max_notes = 0  # Le nombre maximum de notes
        note_range = range(1, 1)  # Plage vide par défaut (ajustée plus tard)

        if module_id:
            module_selected = get_object_or_404(Cours_Module, Id_module=module_id)
            notes_queryset = Notes.objects.filter(matiere_module=module_selected,  etudiant__niveau_etudiant=niveau)
            
            # Désérialiser les notes si elles sont stockées en JSON
            notes = [] 
            
            for note in notes_queryset:
                note_data = {
                    'etudiant': note.etudiant,
                    'notes': json.loads(note.notes) if isinstance(note.notes, str) else note.notes,
                    'moyenne': note.moyenne,
                    'id': note.id,
                }
                notes.append(note_data)
                # Mettre à jour le nombre maximum de notes
                max_notes = max(max_notes, len(note_data['notes']))
            
            # Définir la plage de notes en fonction de max_notes
            note_range = range(1, max_notes + 1)
         # Récupérer les étudiants ayant la même filière et le même niveau
        etudiants_same_filiere_niveau = Etudiant.objects.filter(niveau_etudiant=niveau)
        

        context = {
            
            'modules': modules,
            'module_selected': module_selected,
            'notes': notes,
            'max_notes': max_notes,
            'note_range': note_range,
            'filiere_id': filiere_id,  # Passer l'ID de la filière si nécessaire
            'niveau': niveau,  # Passer le niveau de l'étudiant si nécessaire
            'etudiants': etudiants_same_filiere_niveau,  # Liste des étudiants ayant le même niveau
              # Ajouter l'ID de la note
        }

        return render(request, 'Administration/voir_notes.html', context)
    else:
        return redirect('admin_dashboard')


"""
def voir_notes(request, filiere_id, niveau):
    if request.method == 'GET':
        module_id = request.GET.get('module_id')
        filiere_id = int(filiere_id)

        # Récupérer tous les modules de la filière et du niveau
        modules = Cours_Module.objects.filter(filiere_id=filiere_id, niveau=niveau)

        # Initialiser les variables pour le module sélectionné et les notes
        module_selected = None
        notes = None

        if module_id:
            module_selected = get_object_or_404(Cours_Module, Id_module=module_id)
            notes = Notes.objects.filter(matiere_module_id=module_id).select_related('etudiant')

        context = {
            'modules': modules,
            'module_selected': module_selected,
            'notes': notes,
            'niveau': niveau,
            'filiere_id': filiere_id,
        }

        return render(request, 'Administration/voir_notes.html', context)
    else:
        return redirect('admin_dashboard')
"""

from io import BytesIO  # Importer BytesIO du module io
from django.shortcuts import render
from django.http import HttpResponse
from io import BytesIO
import pandas as pd
from .forms import UploadFileForm
from .models import UploadedFile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib.auth.decorators import login_required
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table

def upload_file(request):
    # ======================= SECTION POST - Traitement du formulaire =======================
    if request.method == 'POST':
        # Création du formulaire avec les données du POST et des fichiers
        form = UploadFileForm(request.POST, request.FILES)
        
        # Vérification si le formulaire est valide
        if form.is_valid():
            # ======================= SECTION SAUVEGARDE DU FICHIER DANS LE MODÈLE =======================
            # Sauvegarder le fichier dans le modèle UploadedFile
            uploaded_file = form.cleaned_data['file']
            uploaded_file_instance = UploadedFile(file=uploaded_file)
            uploaded_file_instance.save()

            # ======================= SECTION TRAITEMENT DU FICHIER EXCEL =======================
            # Lire le fichier Excel téléchargé avec toutes ses feuilles
            excel_file = pd.ExcelFile(uploaded_file)
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)

            # Créer une liste pour les éléments du PDF
            elements = []

            # ======================= SECTION TRAITEMENT DES FEUILLES EXCEL =======================
            for sheet_name in excel_file.sheet_names:
                # Lire chaque feuille dans un DataFrame
                df = excel_file.parse(sheet_name)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                # Remplacer les NaN par des chaînes vides
                df.fillna('', inplace=True)
                # Ajouter un titre pour la feuille
                elements.append(Paragraph(sheet_name, ParagraphStyle(
                    name='Heading1',
                    fontSize=26,
                    leading=20,
                    textColor=colors.darkblue,
                    alignment=1,  # Centrer le texte
                    spaceAfter=12,
                )))
                

                # Préparer les données pour le tableau
                data = [df.columns.to_list()] + df.values.tolist()

                # Créer le tableau
                table = Table(data)  # Ajuste la largeur des colonnes

                # Appliquer un style au tableau
                style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4A86E8")),  # Bleu pour l'en-tête
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texte blanc pour l'en-tête
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ])
                table.setStyle(style)

                # Ajouter le tableau au PDF
                elements.append(table)
                elements.append(Spacer(1, 12))  # Ajouter un espace entre les feuilles
                elements.append(PageBreak())  # Saut de page après chaque feuille

            # ======================= SECTION GÉNÉRATION DU PDF =======================
            # Construire le PDF
            doc.build(elements)

            # ======================= SECTION SAUVEGARDE DU PDF =======================
            # Créer un chemin pour sauvegarder le PDF
            pdf_file_path = f'uploaded_files/{uploaded_file.name.replace(".xlsx", ".pdf")}'

            # Créer un fichier temporaire pour sauvegarder le PDF dans le système
            pdf_file_name = uploaded_file.name.replace(".xlsx", ".pdf")
            pdf_uploaded_file_instance = UploadedFile()
            pdf_uploaded_file_instance.file.save(f'uploaded_files/{pdf_file_name}', buffer, save=True)

            # Sauvegarder le contenu PDF dans le fichier
            with open(pdf_file_path, 'wb') as f:
                f.write(buffer.getvalue())

            # Créer une nouvelle instance de UploadedFile pour le PDF
            uploaded_file_instance = UploadedFile()
            uploaded_file_instance.file.save(uploaded_file.name, uploaded_file, save=True)


            # ======================= SECTION NOTIFICATION =======================
            # Création de la notification
            message = f"Un nouveau emploi du temps a été uploader : {uploaded_file.name}."
            # Récupérer tous les professeurs
            professeurs_list = professeurs.objects.all()
            for prof in professeurs_list:
                # Créer une notification pour chaque professeur
                notification = Notifications(
                    destinataire_prof=prof,
                    message=message
                )
                notification.save()

            # ======================= SECTION MESSAGE DE SUCCÈS =======================
            messages.success(request, "Le fichier PDF a été téléchargé avec succès.")
            # Optionnel : rediriger vers une page de succès ou afficher un message
            return redirect('list_uploaded_files')  # Remplacez par le nom de votre vue
            
    # ======================= SECTION FORMULAIRE PAR DÉFAUT =======================
    else:
        form = UploadFileForm()

    return render(request, 'Administration/upload.html', {'form': form})

@login_required(login_url='login')
def list_uploaded_files(request):
    #files = UploadedFile.objects.all().order_by('-uploaded_at')
    files = UploadedFile.objects.exclude(file__endswith='.pdf').order_by('-uploaded_at')
    return render(request, 'Administration/list_files.html', {'files': files})

#supprimer un fichier de la bd

@login_required(login_url='login')
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file.delete()
    messages.success(request, 'Fichier supprimé avec succès.')
    return redirect('list_uploaded_files')
import pandas as pd
from django.shortcuts import get_object_or_404, render
from PyPDF2 import PdfReader
import os
from django.conf import settings

def display_table(request, file_id):
    # Récupérer l'objet UploadedFile à partir de l'ID du fichier
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path

    # Vérifier l'extension du fichier
    file_extension = os.path.splitext(uploaded_file.file.name)[1].lower()

    if file_extension == '.pdf':
        # Si le fichier est un PDF, l'ouvrir et afficher le contenu
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()  # Extraire le texte du PDF
            #return render(request, 'Administration/display_pdf.html', {'pdf_text': text})
            return redirect(reverse('display_pdf', args=[file_id]))
        except Exception as e:
            return render(request, 'Administration/error.html', {'message': 'Erreur lors de l\'ouverture du PDF', 'error': str(e)})

    elif file_extension in ['.xls', '.xlsx']:
        # Si le fichier est un Excel, le lire avec pandas et afficher sous forme de table HTML
        try:
            df = pd.read_excel(file_path, engine='openpyxl')  # Utiliser openpyxl pour les fichiers .xlsx
            table_html = df.to_html(index=False)  # Convertir le DataFrame en HTML
            return render(request, 'Administration/display_table.html', {'table_html': table_html})
        except Exception as e:
            return render(request, 'Administration/error.html', {'message': 'Erreur lors de l\'ouverture du fichier Excel', 'error': str(e)})

    else:
        return render(request, 'Administration/error.html', {'message': 'Format de fichier non supporté.'})

from PyPDF2 import PdfReader
from django.shortcuts import render

def display_pdf(request, file_id):
       # Récupérer le fichier PDF à partir de la base de données
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)

    # Chemin du fichier PDF
    file_path = uploaded_file.file.path

    # Extraire le texte du PDF
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        pdf_text = ""
        for page in reader.pages:
            # Combine le texte extrait de chaque page
            pdf_text += page.extract_text()

    # Diviser le texte en lignes
    rows = pdf_text.strip().split("\n")

    # Transformer chaque ligne en colonnes (en supposant des séparateurs comme espaces ou tabulations)
    table_data = [row.split() for row in rows if row.strip()]  # Ignorer les lignes vides

    return render(request, 'Administration/display_pdf.html', {'table_data': table_data})



def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # Vérifiez si l'email existe dans la base de données
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                subject = "Réinitialisation de votre mot de passe"
                email_template_name = 'registration/password_reset_email.html'
                c = {
                    'email': email,
                    'domain': get_current_site(request).domain,
                    'site_name': 'Votre Site',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                }
                email_message = render_to_string(email_template_name, c)
                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [email])
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    subject_template_name = 'registration/password_reset_subject.txt'
    token_generator = default_token_generator
    template_name = 'registration/password_reset_form.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    
def test_email_view(request):
    if request.method == 'POST':
        send_mail(
            'Test Email',
            'Ceci est un email de test depuis Django.',
            'bonfilswendtoe@gmail.com',  # Ton adresse Gmail
            ['wendtoezorma@gmail.com'],  # Adresse du destinataire
            fail_silently=False,
        )
        return render(request, 'Administration/test_email.html', {'message': 'Email de test envoyé avec succès!'})
    return render(request, 'Administration/test_email.html')


#voir ses moyenne en tant qu'etudiant 
    #vue pour que les etudiants voi leur notes et moyenne
    from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ScolariteForm,FiltreForm

#pour qu'un etudiant puissent voir ses note
from .models import Etudiant, Notes, Cours_Module

def etudiant_notes(request):
    # Assurez-vous que l'étudiant est connecté et qu'il a une session active
    etudiant_id = request.session.get('etudiant_id')
    if not etudiant_id:
        
        return redirect('etudiant_login')  # Rediriger vers la page de connexion si non authentifié

    etudiant = get_object_or_404(Etudiant, matricule=etudiant_id)
    # Récupérer toutes les notes de l'étudiant
    notes = Notes.objects.filter(etudiant=etudiant)
    
    return render(request, 'Administration/etudiant_notes.html', {'etudiant': etudiant, 'notes': notes})

#afficher tous les modules de la classe deja enregistrer 
def modules_classe(request):
    # Assurez-vous que l'étudiant est connecté et qu'il a une session active
    etudiant_id = request.session.get('etudiant_id')
    if not etudiant_id:
        return redirect('etudiant_login')  # Rediriger vers la page de connexion si non authentifié

    etudiant = get_object_or_404(Etudiant, matricule=etudiant_id)
    # Récupérer tous les modules de la filière de l'étudiant
    modules = Cours_Module.objects.filter(filiere=etudiant.filiere)
    
    return render(request, 'Administration/modules_classe.html', {'etudiant': etudiant, 'modules': modules})
#permet de voir tous les informatons de l'etudiant
def student_profile(request):
    # Récupère l'étudiant connecté à partir de la session
    etudiant = get_object_or_404(Etudiant, matricule=request.session.get('etudiant_id'))
    
    # Passe les informations de l'étudiant au template
    return render(request, 'etudiant_profile.html', {'etudiant': etudiant})


#autocompletition pour la recherche de l etudiant dans la scolarité

def etudiant_autocomplete(request):
    if 'q' in request.GET:
        query = request.GET['q']
        students = Etudiant.objects.filter(nom__icontains=query)[:10]  # Limitez à 10 résultats
        results = [{'id': s.id, 'text': s.nom} for s in students]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

from .models import Etudiant
from dal import autocomplete 

class EtudiantAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        
        

        qs = Etudiant.objects.all()

        # Appliquer un filtre basé sur l'entrée utilisateur
        if self.q:
            qs = qs.filter(nom_etudiant__icontains=self.q)
             # Récupérer et stocker la valeur du champ 'tranches' de la scolarité de chaque étudiant
            

        

        return qs
    def get_result_label(self, item):
        """ Affiche nom + matricule dans la liste déroulante """
        return f"{item.nom_etudiant} ({item.matricule})"

    def get_result_value(self, item):
        """ Retourne l'ID de l'étudiant (ou matricule) """
        return item.matricule

    def render_to_response(self, context):
        """ Format JSON personnalisé avec nom et matricule """
        results = [
            {"id": etudiant.matricule, "text": f"{etudiant.nom_etudiant} II {etudiant.prenom_etudiant} II {etudiant.filiere.nom_filiere} "} 
            for etudiant in context["object_list"]
        ]
        return JsonResponse({"results": results})
    
    



def gestion_scolarite(request):
    filieres = Filiere.objects.all()
    scolarites = Scolarite.objects.select_related('etudiant').all()
    etudiants = Etudiant.objects.all()
    
    total_caisse = apercu_caisse()
    total_etudiants_inscrit = Etudiant.objects.count()
    total_etudiants_solde = Scolarite.objects.filter(Montant_restant=0.0).count()
    date_paiement = datetime.now().strftime('%Y-%m-%d')
    heure_paiement = datetime.now().strftime('%H:%M')
    

    if request.method == 'POST':
        etudiant_id = request.POST.get('etudiant')
        scolarite = Scolarite.objects.filter(etudiant_id=etudiant_id).first()
         # Créer un formulaire de scolarité
        scolarite_form = ScolariteForm(request.POST, instance=scolarite)
        
  
        
        if scolarite_form.is_valid():
            new_scolarite = scolarite_form.save(commit=False)
             # Mettre à jour les valeurs spécifiques sans écraser # Assurez-vous que ce champ existe
             #tranches = new_scolarite.tranches
             # Initialiser une liste vide pour les tranches
            tranches = []
            
           
            for i in range(10):  # Maximum de 10 tranches, ajustable
                tranche_value = request.POST.get(f'tranche_{i+1}', '')
                if tranche_value == '':  # Si la valeur est vide, on remplace par 0
                    tranche_value = 0
                try:
                    tranches.append(float(tranche_value))  # Ajouter la tranche à la liste
                except ValueError:
                    tranches.append(0)  # Remplacer par 0 en cas d'erreur de conversion

           
            new_scolarite.tranches = tranches
            new_scolarite.total = sum(tranches)  # Calculer le total basé sur les tranches
            new_scolarite.montant_total_verse = sum(tranches)
            new_scolarite.Montant_restant = new_scolarite.total - new_scolarite.montant_total_verse
            
            print(new_scolarite.total, new_scolarite.montant_total_verse , new_scolarite.Montant_restant )
             # Cela devrait afficher les tranches stockées dans la BD

            
            new_scolarite.save()
            
         # Après la sauvegarde, nous préparons les données pour le reçu
            context = {
                    'q': etudiant_id,  # Si vous avez besoin du matricule
                    'scolarites': scolarite,
                    'date_paiement': date_paiement,
                    'heure_paiement': heure_paiement,
                }
            
                # Générer le 
              
            print(f'la scolarité stocker : {tranches}')
    
            
            return render(request, 'Administration/recu_paiement.html',context)
                #return redirect('gestion_scolarite')
        
    else:
        scolarite_form = ScolariteForm()

    context = {
        'scolarites': scolarites,
        'etudiants': etudiants,
        'scolarite_form': scolarite_form,
        'filieres': filieres,
        'total_caisse': total_caisse,
        'total_etudiants_inscrit': total_etudiants_inscrit,
        'total_etudiants_solde': total_etudiants_solde,
        'date_paiement': date_paiement,
        'heure_paiement': heure_paiement,
    }
    return render(request, 'Administration/scolarite.html', context)

from django.http import JsonResponse
from django.http import JsonResponse
from .models import Scolarite, Etudiant

def get_scolarite2(request):
    etudiant_id = request.GET.get('etudiant_id')
    
    if not etudiant_id:
        return JsonResponse({'error': 'Paramètre etudiant_id manquant'}, status=400)

    try:
        scolarite = Scolarite.objects.get(etudiant__matricule=etudiant_id)
        tranches = scolarite.tranches  # Supposé être un JSONField sous forme de liste

          
        
        return JsonResponse({
            'tranche_1': tranches[0] if len(tranches) > 0 else 0,
            'tranche_2': tranches[1] if len(tranches) > 1 else 0,
            'tranche_3': tranches[2] if len(tranches) > 2 else 0,
            'tranche_4': tranches[3] if len(tranches) > 0 else 0,
            'tranche_5': tranches[4] if len(tranches) > 1 else 0,
            'tranche_6': tranches[5] if len(tranches) > 2 else 0,
            
            'tranche_7': tranches[6] if len(tranches) > 0 else 0,
            'tranche_8': tranches[7] if len(tranches) > 1 else 0,
            'tranche_9': tranches[8] if len(tranches) > 2 else 0,
            'tranche_10': tranches[9] if len(tranches) > 0 else 0,
            'total': scolarite.total
        })
    except Scolarite.DoesNotExist:
        return JsonResponse({'error': 'Aucune scolarité trouvée pour cet étudiant.'}, status=404)
    

def get_scolarite(request, etudiant_id):
    
    scolarite = Scolarite.objects.filter(etudiant_id=etudiant_id).first()
    
    if scolarite:
        raw_password = scolarite.mdp_etudiant
        return JsonResponse({
            'tranche_1': scolarite.tranche_1,
            'tranche_2': scolarite.tranche_2,
            'tranche_3': scolarite.tranche_3,
            'mot_de_passe': raw_password,
        })
    return JsonResponse({'tranche_1': 0, 'tranche_2': 0, 'tranche_3': 0,'mot_de_passe': None})


def obtenir_informations_etudiant(request):
    if request.method == 'GET':
        etudiant_id = request.GET.get('etudiant_id')
        try:
            scolarite = Scolarite.objects.get(etudiant_id=etudiant_id)
            data = {
                'tranche_1': scolarite.tranche_1,
                'tranche_2': scolarite.tranche_2,
                'tranche_3': scolarite.tranche_3,
            }
            return JsonResponse(data)
        except Scolarite.DoesNotExist:
            return JsonResponse({'error': 'Scolarité non trouvée'}, status=404)


################ Lister les fichiers disponibles pour les etudiants ##########
from django.shortcuts import render
from .models import CoursFichier

def cours_list(request):
    cours_fichiers = CoursFichier.objects.all()
    if request.method == 'POST':
        scolarite_form = ScolariteForm(request.POST)
        if scolarite_form.is_valid():
            scolarite_form.save()
            messages.success(request, 'Scolarité mise à jour avec succès.')
            return redirect('gestion_scolarite')
    else:
        scolarite_form = ScolariteForm()

    return render(request, 'Administration/cours_list.html', {'cours_fichiers': cours_fichiers,})


################ Les informations sur l'app mobile  ################



def infos(request):
    # Récupère toutes les informations enregistrées
    infos_list = Infos.objects.all()
    
    if request.method == 'POST':
        # Inclure request.FILES pour gérer les fichiers téléchargés
        form = Infos_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
                
            return redirect('voir_infos')
    else:
        form = Infos_Form()

    return render(request, 'Administration/infos.html', {'form': form, 'infos_list': infos_list})

def voir_info(request):
    if request.method == 'POST':
        # Suppression d'un message
        info_id = request.POST.get('id_infos')  # Assurez-vous que c'est 'id_infos'
        if info_id:
            info = get_object_or_404(Infos, id_infos=info_id)
            info.delete()
            messages.success(request, 'Le message a été supprimé avec succès.')
            return redirect('infos')  # Redirigez vers la même page après la suppression

    infos = Infos.objects.all().order_by('-date_creation')  # Récupérer toutes les instances d'Infos
    return render(request, 'Administration/voir_informations.html', {'infos': infos})



############# fichiers ###########
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CoursFichierForm

@login_required
def upload_cours(request):
    if request.method == 'POST':
        form = CoursFichierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fichier ajouté avec succès.')
            return redirect('cours_list')  # Redirige vers une page liste des cours après le téléchargement
    else:
        form = CoursFichierForm()
    return render(request, 'Administration/upload_cours.html', {'form': form})

from django.db.models import Q

@login_required
def rechercher_etudiants(request):
    query = request.GET.get('query', '').strip()
    if query:
        # Filtrage par plusieurs champs
        etudiants = Etudiant.objects.filter(
            Q(nom_etudiant__icontains=query) |
            Q(prenom_etudiant__icontains=query) |
            Q(email_etudiant__icontains=query) |
            Q(telephone_etudiant__icontains=query) |
            Q(lieu_naiss_etudiant__icontains=query) |
            Q(nationalite_etudiant__icontains=query) |
            Q(niveau_etudiant__icontains=query) |
            Q(annee_academique_etudiant__icontains=query)
            ).distinct()
        no_results = not etudiants.exists()
    else:
        etudiants = Etudiant.objects.all()
        no_results = False  # Pas de message si la recherche est vide
    
    return render(request, 'Administration/rechercher_etudiants.html', {'etudiants': etudiants, 'no_results': no_results , 'query': query})

from django.http import JsonResponse
from .models import Etudiant

def recherche_etudiants_pour_solarite(request):
    if 'term' in request.GET:
        etudiants = Etudiant.objects.filter(nom__icontains=request.GET.get('term')) | Etudiant.objects.filter(prenom__icontains=request.GET.get('term'))
        etudiant_list = list(etudiants.values('id', 'nom', 'prenom'))
        return JsonResponse(etudiant_list, safe=False)


def prof_dashboard(request):
    return render(request, 'prof/prof_dashboard.html')


def recherche_etudiant(request):
    if request.method == 'POST':
        form = RechercheEtudiantForm(request.POST)
        if form.is_valid():
            matricule = form.cleaned_data['matricule']
            semestre = form.cleaned_data['semestre']  # Récupérer le semestre choisi
            return redirect('generer_bulletin', matricule=matricule, semestre=semestre)
            #matricule = form.cleaned_data['matricule']
            #return redirect('generer_bulletin', matricule=matricule)  # Rediriger vers le bulletin de l'étudiant
    else:
        form = RechercheEtudiantForm()

    return render(request, 'Administration/recherche_etudiant.html', {'form': form})


from django.http import JsonResponse
from .models import Etudiant

def recherche_etudiant_scolarite(request):
    term = request.GET.get('term', '')  # Récupérer le terme de recherche
    if term:
        etudiants = Etudiant.objects.filter(nom__icontains=term)  # Recherche des étudiants par nom
        results = [{'id': etudiant.id, 'nom': etudiant.nom, 'prenom': etudiant.prenom} for etudiant in etudiants]
    else:
        results = []
    return JsonResponse(results, safe=False)


def  generer_bulletin(request, matricule, semestre):
     # Récupérer l'étudiant en fonction de son matricule
    etudiant = get_object_or_404(Etudiant, matricule=matricule)
    


  
    # Récupérer les notes de l'étudiants
    #notes = Notes.objects.filter(etudiant=etudiant).select_related('matiere_module')
    notes = Notes.objects.filter(
        etudiant=etudiant, 
        matiere_module__semestre=semestre  # Filtrer les modules par semestre
    ).select_related('matiere_module')
      # Récupérer le semestre depuis les paramètres GET (par exemple, ?semestre=SEMESTRE 1)
    #semestre = request.GET.get('semestre')  # Défaut à SEMESTRE 1 si non fourni
    #semestre = notes.first().matiere_module.semestre  # Récupérer le semestre du premier module
    semestre = notes.first().matiere_module.semestre if notes.exists() else "Non spécifié"


     # Séparer les matières en fonction de l'unité d'enseignement
    #notes_fondamentale = notes.filter(matiere_module__unite_enseignement='unite_fondamentale')
    #notes_transversale = notes.filter(matiere_module__unite_enseignement='unite_transversale')
    notes_fondamentale = notes.filter(matiere_module__unite_enseignement='FONDAMENTALE')    
    notes_transversale = notes.filter(matiere_module__unite_enseignement='TRANSVERSALE')

    
    # Calcul des moyennes par unité d'enseignement

    def calculer_moyenne_unite(notes_unite):
        total_notes_unite = sum(note.moyenne * note.matiere_module.credit_module for note in notes_unite)
        total_credits_unite = sum(note.matiere_module.credit_module for note in notes_unite)
       
        if total_credits_unite > 0:
            return total_notes_unite / total_credits_unite
        else:
            return 0.0

    moyenne_fondamentale = calculer_moyenne_unite(notes_fondamentale)
    moyenne_transversale = calculer_moyenne_unite(notes_transversale)
   
    # Calculer la moyenne générale
    total_notes_ponderees = sum(note.moyenne * note.matiere_module.credit_module for note in notes)
    total_credits = sum(note.matiere_module.credit_module for note in notes)
    
    if total_credits > 0:
        moyenne_generale = total_notes_ponderees / total_credits
    else:
        moyenne_generale = 0.0
    
    # Déterminer la mention en fonction de la moyenne générale
    if moyenne_generale >= 16:
        mention = "Très Bien"
        decision_jury = "Admis"
    elif moyenne_generale >= 14:
        mention = "Bien"
        decision_jury = "Admis"
    elif moyenne_generale >= 12:
        mention = "Assez-Bien"
        decision_jury = "Admis"
    else:
        mention = "Insuffisant"
        decision_jury = "Ajourné"
    #notes_ponderees = [(note, note.moyenne * note.matiere_module.credit_module) for note in notes],
    notes_ponderees = [(note, note.moyenne * note.matiere_module.credit_module) for note in notes]
    # Contexte des variables à passer au template
    context = {
        
        'etudiant': etudiant,
        #'matiere': notes,
        'notes': notes,  # Liste des notes avec les modules associés
        'notes_ponderees': notes_ponderees,
        'moyenne_generale': round(moyenne_generale, 2),
        'moyenne_fondamentale': round(moyenne_fondamentale, 2),
        'moyenne_transversale': round(moyenne_transversale, 2),
        'semestre': semestre,
        'mention': mention,
        'decision_jury': decision_jury,
        'total_credits': total_credits,
        'directeur_name': 'Dr. Frédéric BATIONO',
        'directeur_signature_url': '/static/Administration/images/signature_directeur.png',
        'header_image_url': '/static/Administration/images/header_image.jpg',
        'footer_image_url': '/static/Administration/images/footer_image.jpg',
        'institution_adresse': '01 BP 6445 Ouagadougou 01',
        'institution_tel': '+226 25375735 / 51893535 / 79802980',
    }

    return render(request, 'Administration/bulletin.html', context)
    


def demander_matricule(request):
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        # Redirige vers la vue du profil de l'étudiant avec le matricule
        return redirect('profil_etudiant_cursus', matricule=matricule)
    return render(request, 'Administration/demander_matricule.html')

from django.shortcuts import render, get_object_or_404
from .models import Etudiant, Notes, Cours_Module, professeurs

def profil_etudiant(request, matricule):
    # Récupérer l'étudiant via son matricule
    etudiant = get_object_or_404(Etudiant, matricule=matricule)
    
    # Récupérer l'année académique de l'étudiant
    annee_academique = etudiant.annee_academique_etudiant
    
    # Récupérer toutes les notes de l'étudiant, indépendamment des modules suivis avant ou après son inscription
    notes = Notes.objects.filter(etudiant=etudiant)
    
    # Récupérer tous les modules pour la filière et le niveau de l'étudiant
    cours_modules = Cours_Module.objects.filter(filiere=etudiant.filiere, niveau=etudiant.niveau_etudiant)
    
    # Récupérer tous les enseignants pour les modules que l'étudiant a suivis
    enseignants = professeurs.objects.filter(modules__in=cours_modules)
    # Pour chaque note, récupérer les enseignants associés au module
   
    context = {
        'etudiant': etudiant,
        'notes': notes,
        'cours_modules': cours_modules,
        'enseignants': enseignants,
        'annee_academique': annee_academique
    }

    return render(request, 'Administration/profil_etudiant.html', context)



def reinscription_etudiant(request):
    etudiant = None  # Initialiser l'étudiant à None au début

    if request.method == 'POST':
        # Vérifier quel formulaire est soumis en fonction du champ 'niveau_etudiant'
        if 'niveau_etudiant' in request.POST and 'annee_academique' in request.POST:
            # Traitement du formulaire de réinscription d'étudiant
            matricule = request.POST.get('matricule')  # Récupérer le matricule caché dans le formulaire
            etudiant = get_object_or_404(Etudiant, matricule=matricule)

            # Récupérer le nouveau niveau et l'année académique
            nouveau_niveau = request.POST.get('niveau_etudiant')
            nouvelle_annee_academique = request.POST.get('annee_academique')

            # Vérification de la scolarité précédente
            scolarite_precedente = Scolarite.objects.filter(etudiant=etudiant).order_by('-annee_academique').first()

            if scolarite_precedente and scolarite_precedente.Montant_restant == 0.0:
                # Exporter les anciennes données au format JSON
                ancienne_data = {
                    'etudiant_id': etudiant.matricule,
                    'niveau_etudiant': etudiant.niveau_etudiant,
                    'annee_academique': scolarite_precedente.annee_academique,
                    'total': scolarite_precedente.total,
                    'Montant_restant': scolarite_precedente.Montant_restant,
                    'tranche_1': scolarite_precedente.tranche_1,
                    'tranche_2': scolarite_precedente.tranche_2,
                    'tranche_3': scolarite_precedente.tranche_3,
                }
                
                # Enregistrer les anciennes données dans un fichier JSON
                #with open(f"ancienne_scolarite_{etudiant.matricule}.json", "w") as json_file:
                 #   json.dump(ancienne_data, json_file)
                 # Enregistrer les anciennes données dans un fichier JSON dans le répertoire media/js_scolarite/
                js_scolarite_dir = os.path.join(settings.MEDIA_ROOT, 'js_scolarite')
                file_path = os.path.join(js_scolarite_dir, f"ancienne_scolarite_{etudiant.matricule}.json")
                with open(file_path, "w") as json_file:
                    json.dump(ancienne_data, json_file)

                # Mettre à jour les informations de l'étudiant
                etudiant.niveau_etudiant = nouveau_niveau
                etudiant.annee_academique_etudiant = nouvelle_annee_academique

                # Créer une nouvelle scolarité pour l'étudiant
                nouvelle_scolarite = Scolarite(
                    etudiant=etudiant,
                    annee_academique=nouvelle_annee_academique,
                    tranche_1=0.0,
                    tranche_2=0.0,
                    tranche_3=0.0,
                )

                # Calculer le total basé sur l'étudiant actuel
                nouvelle_scolarite.total = nouvelle_scolarite.calculate_total()  # Utiliser l'instance pour calculer le total
                nouvelle_scolarite.Montant_restant = nouvelle_scolarite.total
              
                # Enregistrer les modifications de l'étudiant et la nouvelle scolarité
                nouvelle_scolarite.save()
                scolarite_precedente.delete()


                etudiant.save()
                

                # Message de succès et redirection
                messages.success(request, f"L'étudiant {etudiant.nom_etudiant} a été réinscrit avec succès pour {nouvelle_annee_academique}.")
                return redirect('admin_dashboard')
            else:
                messages.error(request, f"L'étudiant {etudiant.nom_etudiant} n'a pas soldé sa scolarité pour l'année précédente.")
                return redirect('gestion_scolarite')

        # Si le formulaire de recherche d'étudiant est soumis
        elif 'matricule' in request.POST:
            matricule = request.POST.get('matricule')
            if matricule:
                etudiant = get_object_or_404(Etudiant, matricule=matricule)
            else:
                messages.error(request, "Veuillez entrer un matricule valide.")
                return redirect('reinscription_etudiant')

    context = {
        'etudiant': etudiant,
        'niveaux': ['LICENCE1', 'LICENCE2', 'LICENCE3', 'MASTER1', 'MASTER2', 'DOCTORAT'],
    }
    return render(request, 'Administration/reinscription_etudiant.html', context)


def recuperer_notifications(request):
    # Récupère l'administrateur connecté
    administrateur = request.user
    
    # Filtre les notifications pour cet administrateur
    notifications = Notifications.objects.filter(destinataire_admin=administrateur).order_by('-date')
    notifications.filter(lu=False).update(lu=True)

    context = {
        'notifications': notifications
    }

    return render(request, 'Administration/notifications.html', context)





def creer_notification(destinataire_admin=None, destinataire_prof=None, message=""):
    if not destinataire_admin and not destinataire_prof:
        raise ValueError("Un destinataire doit être spécifié.")

    # Génération automatique du message basé sur l'événement
    messages = f"Nouvelle notification liée à l'événement : {message}"

    Notifications.objects.create(
        destinataire_admin=destinataire_admin,
        destinataire_prof=destinataire_prof,
        message=messages
    )
    



def notifications_non_lues_count_admin(request):
    """
    Retourne le nombre de notifications non lues pour l'utilisateur connecté.
    """
    user = request.user  # Utilisateur actuellement connecté
    
    # Récupérer les notifications non lues
    notifications_non_lues = Notifications.objects.filter(destinataire_admin=user, lu=False)
    
    # Créer une liste des messages non lus
    messages_non_lus = [notification.message for notification in notifications_non_lues]
    
    # Retourner le nombre et les messages non lus dans un JsonResponse
    return JsonResponse({'notifications_non_lues': len(messages_non_lus), 'messages_non_lus': messages_non_lus})
