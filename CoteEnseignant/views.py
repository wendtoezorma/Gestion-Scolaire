from django.shortcuts import render, redirect
from .forms import *
from Administration.models import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from Administration.models import professeurs
from .login_required import * 

# Create your views here.
def connexion_Prof(request):
    if request.method == 'POST':
        form = ProfesseurLoginForm(request.POST)
        if form.is_valid():
            email_prof = form.cleaned_data['email_prof']
            mot_de_passe = form.cleaned_data['mdp_prof']
            try:
                professeur =  professeurs.objects.get(email_prof=email_prof)
                if professeur.check_password(mot_de_passe):
                    # Authentifier le professeur et créer une session
                    request.session['professeur_id'] = professeur.Id_prof
                    return redirect('Professeur_dashboard')  # Redirige vers le tableau de bord des professeurs
                else:
                    form.add_error('mdp_prof', 'Mot de passe incorrect')
            except professeur.DoesNotExist:
                form.add_error('email_prof', 'Email non trouvé')
    else:
        form = ProfesseurLoginForm()
    return render(request, 'prof/professeur_login.html', {'form': form})

@professeur_login_required
def Professeur_dashboard(request):
    return render(request, 'prof/prof_dashboard.html')
@professeur_login_required
def Voir_notes(request):
    professeur_id = request.session.get('professeur_id')
    filieres = Filiere.objects.all()
    niveaux = Etudiant.objects.values_list('niveau_etudiant', flat=True).distinct()
    return render(request, 'prof/tri_pour_classe_pour_prof.html', {'filieres': filieres, 'niveaux': niveaux,'professeurs_id': professeur_id})



@professeur_login_required
def afficher_classe(request, filiere_id, niveau, professeur_id):
    # Récupérer le professeur
    try:
        # Récupérer le professeur
        professeur = professeurs.objects.get(Id_prof=professeur_id)
    except professeurs.DoesNotExist:
        return render(request, 'Administration/classe.html', {
            'error_message': "Le professeur n'existe pas."
        })
    
    # Vérifier si le professeur enseigne un cours dans la filière demandée
    modules = Cours_Module.objects.filter(filiere_id=filiere_id, professeur_id=professeur.Id_prof,niveau=niveau)
    #filiere = modules.first().filiere  # Récupérer la filière du premier module trouvé
    filiere = getattr(modules.first(), 'filiere', None)
    if not modules.exists():
        return render(request, 'Prof/classes.html', {
            'error_message': "Vous n'avez pas le droit d'ouvrir cette classe."
        })

    # Récupérer les étudiants et les modules pour la filière et le niveau donnés
    etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
    modules = modules.filter(niveau=niveau)  # Ajouter un champ niveau dans Cours_Module si nécessaire

    context = {
        'etudiants': etudiants,
        'filiere_id': filiere_id,
        'niveau': niveau,
        'nom_filiere': filiere.nom_filiere,
        'modules': modules,
    }
    return render(request, 'prof/classes.html', context)


def select_module_pour_prof(request, filiere_id, niveau):
    modules = Cours_Module.objects.filter(filiere_id=filiere_id)
    context = {
        'modules': modules,
        'filiere_id': filiere_id,
        'niveau': niveau,
        
    }
    return render(request, 'Prof/select_module_prof.html', context)




   


from Administration.forms import *
@professeur_login_required
def upload_cours_prof(request):
    if request.method == 'POST':
        form = CoursFichierForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cours_list_prof')  # Redirige vers une page liste des cours après le téléchargement
    else:
        form = CoursFichierForm()
    return render(request, 'prof/upload_cours_prof.html', {'form': form})


@professeur_login_required
def list_uploaded_files_prof(request):
    files = UploadedFile.objects.all()
    return render(request, 'prof/list_files_prof.html', {'files': files})

@professeur_login_required
def cours_list_prof(request):
    cours_fichiers = CoursFichier.objects.all()
    if request.method == 'POST':
        scolarite_form = ScolariteForm(request.POST)
        if scolarite_form.is_valid():
            scolarite_form.save()
            #messages.success(request, 'Scolarité mise à jour avec succès.')
            return redirect('gestion_scolarite')
    else:
        scolarite_form = ScolariteForm()

    return render(request, 'prof/cours_list_prof.html', {'cours_fichiers': cours_fichiers,})


import pandas as pd
@professeur_login_required
def display_table_prof(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    #file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_excel.xlsx')
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)

    # Convert DataFrame to HTML table
    table_html = df.to_html(index=False)

    return render(request, 'prof/display_table_prof.html', {'table_html': table_html})

from django.contrib import messages

def creer_note_prof(request):
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
        
        return render(request, 'prof/add_note_prof.html', context)
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
        return redirect('Professeur_dashboard')  # Rediriger vers une page de succès ou une autre page appropriée 
    
def voir_notes_prof(request, filiere_id, niveau):
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
        
        return render(request, 'prof/voir_notes_prof.html', context)
    else:
        return redirect('admin_dashboard')
    
def modifier_note_prof(request, note_id):
    note = get_object_or_404(Notes, Id_note=note_id)
    
    if request.method == 'POST':
        note1_str = request.POST.get('note1', '')
        note2_str = request.POST.get('note2', '')
        
        try:
            note.Note1 = float(note1_str.replace(',', '.'))
            note.Note2 = float(note2_str.replace(',', '.'))
            note.save()
            messages.success(request, 'La note a été modifiée avec succès.')
            return redirect('Professeur_dashboard')
        except ValueError:
            messages.error(request, 'Veuillez saisir des nombres valides pour les notes.')
            # Gérer l'erreur ici, peut-être rediriger vers une page d'erreur ou afficher un message
    
    context = {
        'note': note
    }
    return render(request, 'prof/modifier_note_prof.html', context)


def logout_prof(request):
    if 'professeur_id' in request.session:
        del request.session['professeur_id']  # Supprimer la session du professeur
    return redirect('connexion_Prof')  # Rediriger vers la page de connexion