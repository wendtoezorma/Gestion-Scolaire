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

#debut

from .decorators import admin_required, student_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import *
from .forms import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
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



# Create your views here.
def index(request):
    return render(request,"Administration/index.html")


def connexion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            email = form.cleaned_data.get('email')
            mot_de_passe = form.cleaned_data.get('mot_de_passe')
            try:
                user = Administration.objects.get(email=email,nom=nom) 
                if mot_de_passe == user.mot_de_passe and nom == user.nom:
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

#@login_required(login_url='connexion')
def admin_dashboard (request):
    total_etudiants = Etudiant.objects.count()
    total_etudiants_masculin = Etudiant.objects.filter(sexe_etudiant='Masculin').count()
    total_etudiants_feminin = Etudiant.objects.filter(sexe_etudiant='Feminin').count()
    total_professeurs = professeurs.objects.count()
    total_filieres = Filiere.objects.count()
    total_etudiants_connecter = Etudiant.objects.filter(Connecter=True).count()


    context = {
        'total_etudiants': total_etudiants,
        'total_etudiants_masculin': total_etudiants_masculin,
        'total_etudiants_feminin': total_etudiants_feminin,
        'total_professeurs': total_professeurs,
        'total_filieres': total_filieres,
        'total_etudiants_connecter':total_etudiants_connecter
    }
    return render(request,"Administration/admin_dashboard.html",context)


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Etudiant
from .forms import EtudiantCreationForm, EtudiantLoginForm, UpdatePasswordForm
from .paswords_generators import generateur_mdp

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


def student_dashboard(request):

    return render(request, 'Administration\student_dashboard.html')
    

#vue pour l'enregistrement d'un cours

#creer une filiere 

def creer_filiere(request):
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Rediriger vers le tableau de bord administrateur
    else:
        form = FiliereForm()
    return render(request, 'Administration/creer_filiere.html', {'form': form})


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


def creer_note(request):
    if request.method == 'GET':
        filiere_id = request.GET.get('filiere_id')
        niveau = request.GET.get('niveau')
        module_id = request.GET.get('module_id')
        etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
        module = Cours_Module.objects.get(Id_module=module_id)
        
        context = {
            'etudiants': etudiants,
            'module': module,
            'filiere_id': filiere_id,
            'niveau': niveau
        }
        return render(request, 'Administration/add_note.html', context)
    elif request.method == 'POST':
        module_id = request.POST.get('module_id')
        etudiants = request.POST.getlist('etudiant_id')
        notes1 = request.POST.getlist('note1')
        notes2 = request.POST.getlist('note2')
        
        for etudiant_id, note1, note2 in zip(etudiants, notes1, notes2):
            note = Notes(
                etudiant_id=etudiant_id,
                matiere_module_id=module_id,
                Note1=float(note1),
                Note2=float(note2)
            )
            note.save()
        messages.success(request, 'Les notes ont été enregistrées avec succès.')
        return redirect('admin_dashboard')  # Rediriger vers une page de succès ou une autre page appropriée


def liste_etudiants_par_classe(request, filiere_id, niveau):
    etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
    context = {
        'etudiants': etudiants,
        'filiere_id': filiere_id,
        'niveau': niveau,
    }
    return render(request, 'Administration/classe.html', context)




#selectionner le niveau et la filiere 
def tri_pour_classe(request):
    filieres = Filiere.objects.all()
    niveaux = Etudiant.objects.values_list('niveau_etudiant', flat=True).distinct()
    return render(request, 'Administration/tri_pour_classe.html', {'filieres': filieres, 'niveaux': niveaux})


 



def select_module(request, filiere_id, niveau):
    modules = Cours_Module.objects.filter(filiere_id=filiere_id)
    context = {
        'modules': modules,
        'filiere_id': filiere_id,
        'niveau': niveau,
    }
    return render(request, 'Administration/select_module.html', context)




def creer_note(request):
    if request.method == 'GET':
        filiere_id = request.GET.get('filiere_id')
        niveau = request.GET.get('niveau')
        module_id = request.GET.get('module_id')
        etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
        module = Cours_Module.objects.get(Id_module=module_id)
        
        context = {
            'etudiants': etudiants,
            'module': module,
            'filiere_id': filiere_id,
            'niveau': niveau
        }
        return render(request, 'Administration/add_note.html', context)
    elif request.method == 'POST':
        module_id = request.POST.get('module_id')
        etudiants = request.POST.getlist('etudiant_id')
        notes1 = request.POST.getlist('note1')
        notes2 = request.POST.getlist('note2')
        
        for etudiant_id, note1, note2 in zip(etudiants, notes1, notes2):
            note = Notes(
                etudiant_id=etudiant_id,
                matiere_module_id=module_id,
                Note1=float(note1),
                Note2=float(note2)
            )
            note.save()
        messages.success(request, 'Les notes ont été enregistrées avec succès.')
        return redirect('admin_dashboard')  # Rediriger vers une page de succès ou une autre page appropriée
    

def liste_etudiants_par_classe(request, filiere_id, niveau):
    etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
    modules = Cours_Module.objects.filter(filiere_id=filiere_id)
    context = {
        'etudiants': etudiants,
        'filiere_id': filiere_id,
        'niveau': niveau,
        'modules': modules,
    }
    return render(request, 'Administration/classe.html', context)


#selectionner le niveau et la filiere 

def tri_pour_classe(request):
    filieres = Filiere.objects.all()
    niveaux = Etudiant.objects.values_list('niveau_etudiant', flat=True).distinct()
    return render(request, 'Administration/tri_pour_classe.html', {'filieres': filieres, 'niveaux': niveaux})

# vue pour afficher la moyenne d'un etudiant 

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


def modifier_note(request, note_id):
    note = get_object_or_404(Notes, Id_note=note_id)
    
    if request.method == 'POST':
        note1_str = request.POST.get('note1', '')
        note2_str = request.POST.get('note2', '')
        
        try:
            note.Note1 = float(note1_str.replace(',', '.'))
            note.Note2 = float(note2_str.replace(',', '.'))
            note.save()
            messages.success(request, 'La note a été modifiée avec succès.')
            return redirect('admin_dashboard')
        except ValueError:
            messages.error(request, 'Veuillez saisir des nombres valides pour les notes.')
            # Gérer l'erreur ici, peut-être rediriger vers une page d'erreur ou afficher un message
    
    context = {
        'note': note
    }
    return render(request, 'Administration/modifier_note.html', context)

def voir_notes(request, filiere_id, niveau):
    if request.method == 'GET':
        module_id = request.GET.get('module_id')
        filiere_id = int(filiere_id)
        
        # Récupérer tous les modules pour cette filière
        modules = Cours_Module.objects.filter(filiere_id=filiere_id)
        
        # Récupérer le module sélectionné
        module_selected = None
        notes = None
        
        if module_id:
            module_selected = get_object_or_404(Cours_Module, Id_module=module_id)
            notes = Notes.objects.filter(matiere_module_id=module_id).select_related('etudiant')
        
        context = {
            'modules': modules,
            'module_selected': module_selected,
            'notes': notes,
        }
        
        return render(request, 'Administration/voir_notes.html', context)
    else:
        return redirect('admin_dashboard')





import pandas as pd
from django.http import HttpResponse
from .models import Emploi
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.shortcuts import render
from .forms import GenerateTimetableForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle file upload
            file = request.FILES['file']
            df = pd.read_excel(file)

            # Remplacer les NaN par des chaînes vides
            df.fillna('', inplace=True)

            # Créer un buffer pour sauvegarder le PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)

            # Préparer les données pour le tableau
            data = [df.columns.to_list()] + df.values.tolist()

            # Créer le tableau
            table = Table(data)

            # Appliquer un style au tableau
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)

            # Construire le PDF
            elements = []
            elements.append(table)
            doc.build(elements)

            # Créer une réponse HTTP avec le contenu du PDF
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="fichier_modifié.pdf"'

            return response
    else:
        form = UploadFileForm()
    return render(request, 'Administration/upload.html', {'form': form})

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from django.conf import settings

def display_table(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_excel.xlsx')
    df = pd.read_excel(file_path)

    # Convert DataFrame to HTML table
    table_html = df.to_html(index=False)

    return render(request, 'display_table.html', {'table_html': table_html})
