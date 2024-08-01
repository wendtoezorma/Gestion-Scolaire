from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from .models import Etudiant
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

def index(request):
    return render(request,"Administration/index.html")




from django.contrib.auth import authenticate, login  # Importer le login et authenticate
from django.contrib import messages  # Importer messages

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


class CustomLogoutView(LogoutView):
    template_name = None
    success_url = reverse_lazy('home')

# la page ou il y aura tous les elements concernant l'admin

@login_required(login_url='login')
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



@login_required(login_url='login')
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
            return redirect('admin_dashboard')  # Rediriger vers le tableau de bord administrateur
    else:
        form = FiliereForm()
    return render(request, 'Administration/creer_filiere.html', {'form': form})

@login_required(login_url='login')
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
@login_required(login_url='login') 
def creer_professeur(request):
    if request.method == 'POST':
        form = ProfesseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Rediriger vers la liste des professeurs après la création réussie
    else:
        form = ProfesseurForm()
    return render(request, 'Administration/creer_professeur.html', {'form': form})

@login_required(login_url='login')
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



@login_required(login_url='login')
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
    
@login_required(login_url='login')
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
@login_required(login_url='login')
def tri_pour_classe(request):
    filieres = Filiere.objects.all()
    niveaux = Etudiant.objects.values_list('niveau_etudiant', flat=True).distinct()
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

@login_required(login_url='login')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Sauvegarder le fichier dans le modèle UploadedFile
            uploaded_file = form.cleaned_data['file']
            uploaded_file_instance = UploadedFile(file=uploaded_file)
            uploaded_file_instance.save()

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
# afficher les fichier deja uploader

@login_required(login_url='login')
def list_uploaded_files(request):
    files = UploadedFile.objects.all()
    return render(request, 'Administration/list_files.html', {'files': files})

#supprimer un fichier de la bd

@login_required(login_url='login')
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file.delete()
    messages.success(request, 'Fichier supprimé avec succès.')
    return redirect('list_uploaded_files')

def display_table(request,file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    #file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_excel.xlsx')
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)

    # Convert DataFrame to HTML table
    table_html = df.to_html(index=False)

    return render(request, 'Administration/display_table.html', {'table_html': table_html})
 ### tous ece qui concerne le mdp oublier 


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

def gestion_scolarite(request):
    if request.method == 'POST':
        form = ScolariteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scolarité mise à jour avec succès.')
            return redirect('gestion_scolarite')
    else:
        form = ScolariteForm()
    
    return render(request, 'Administration/scolarite.html', {'form': form})

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
################### liste etudiants ####################

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ScolariteForm
from .models import Etudiant, Filiere
from.apperçu import apercu_caisse
def gestion_scolarite(request):
    filieres = Filiere.objects.all()
    etudiants = Etudiant.objects.all()
    scolarites = Scolarite.objects.all()
    
    total_caisse=apercu_caisse()
    total_etudiants_inscrit=Etudiant.objects.count()
    total_etudiants_solde=Scolarite.objects.filter(Montant_restant=0.0).count()
    if request.method == 'POST':
        scolarite_form = ScolariteForm(request.POST)
        if scolarite_form.is_valid():
            scolarite_form.save()
            messages.success(request, 'Scolarité mise à jour avec succès.')
            return redirect('gestion_scolarite')
    else:
        scolarite_form = ScolariteForm()

    return render(request, 'Administration/scolarite.html', {
        'scolarite_form': scolarite_form,
        'etudiants': etudiants,
        'filieres': filieres,
        'total_caisse': total_caisse,
        'total_etudiants_inscrit': total_etudiants_inscrit,
        'total_etudiants_solde': total_etudiants_solde,
        'scolarites': scolarites,
    })


