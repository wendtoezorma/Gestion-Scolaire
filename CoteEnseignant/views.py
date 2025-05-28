from django.shortcuts import render, redirect
from .forms import *
from Administration.models import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from Administration.models import *
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
    #taches = Tache.objects.all()
    #taches = Tache.objects.filter(professeur=request.user.professeur)
     # Vérifiez si l'utilisateur est authentifié via la session
    if 'professeur_id' in request.session:
        professeur_id = request.session['professeur_id']
        
        # Récupérer le professeur en utilisant l'ID de la session
        try:
            professeur = professeurs.objects.get(Id_prof=professeur_id)
            
            # Filtrer les tâches associées à ce professeur
            taches = Tache.objects.filter(professeur=professeur)
            
        except professeurs.DoesNotExist:
            taches = None  # Si le professeur n'existe pas, pas de tâches
    context = {
        'taches': taches,
        
    } 
    return render(request, 'prof/prof_dashboard.html',context)


@professeur_login_required
def Voir_notes(request):
    professeur_id = request.session.get('professeur_id')
    filieres = Filiere.objects.all()
    niveaux = Etudiant._meta.get_field('niveau_etudiant').choices
    
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
    #print(f"filiere_id: {filiere_id}, professeur_id: {professeur.Id_prof}, niveau: {niveau}")
    modules = Cours_Module.objects.filter(filiere_id=filiere_id, professeur_id=professeur.Id_prof,niveau=niveau)
    #filiere = modules.first().filiere  # Récupérer la filière du premier module trouvé
    #print(modules)
    filiere = getattr(modules.first(), 'filiere', None)
    #print(filiere)
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
        'professeur_id' : professeur_id 
    }
    return render(request, 'prof/classes.html', context)


def select_module_pour_prof(request, filiere_id, niveau):
    professeur_id = request.session.get('professeur_id')
    modules = Cours_Module.objects.filter(filiere_id=filiere_id, professeur_id= professeur_id)
    context = {
        'modules': modules,
        'filiere_id': filiere_id,
        'niveau': niveau,
        
    }
    return render(request, 'Prof/select_module_prof.html', context)




   


from Administration.forms import *
@professeur_login_required
def upload_cours_prof(request):
    # Vérifier si le professeur est connecté (ID du professeur dans la session)
    professeur_id = request.session.get('professeur_id')
    
    if professeur_id:
        # Si le professeur est connecté, préremplir le champ professeur dans le formulaire
        if request.method == 'POST':
            form = CoursFichierForm(request.POST, request.FILES, professeur_id=professeur_id)
            if form.is_valid():
                form.save()
                return redirect('cours_list_prof')  # Redirige vers la liste des cours
        else:
            form = CoursFichierForm(professeur_id=professeur_id)
    

    return render(request, 'prof/upload_cours_prof.html', {'form': form})




# def upload_cours_prof(request):
#     if request.method == 'POST':
#         form = CoursFichierForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('cours_list_prof')  # Redirige vers une page liste des cours après le téléchargement
#     else:
#         form = CoursFichierForm()
#     
#     return render(request, 'prof/upload_cours_prof.html', {'form': form})


@professeur_login_required
def list_uploaded_files_prof(request):
    #files = UploadedFile.objects.all()
    files = UploadedFile.objects.exclude(file__endswith='.pdf').order_by('-uploaded_at')
    return render(request, 'prof/list_files_prof.html', {'files': files})

@professeur_login_required
def cours_list_prof(request):
    # Récupérer l'ID du professeur depuis la session

    professeur_id = request.session.get('professeur_id')

    if not professeur_id:
        # Si aucun ID de professeur n'est trouvé dans la session, rediriger ou afficher une erreur
        return redirect('connexion_Prof')  
    #cours_fichiers = CoursFichier.objects.all()
     # Filtrer les fichiers liés au professeur connecté


    cours_fichiers = CoursFichier.objects.filter(professeur_id=professeur_id)
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




from django.urls import reverse

def creer_note_prof(request):
    notes_existantes = {} 
    if request.method == 'POST':
        etudiants = []
        notes_data = {}
        range_list = range(1, 6)

        # Récupérer les matricules des étudiants
        for key in request.POST:
            if key.startswith('etudiant_matricules_'):
                matricule = request.POST.get(key)
                etudiants.append(matricule)

        # Récupérer les notes pour chaque étudiant
        for etudiant in etudiants:
            notes_data[etudiant] = []
            for i in range_list:
                note_key = f'note_{etudiant}_{i}'
                coef_key = f'coef_{etudiant}_{i}'

                note_value = request.POST.get(note_key, '0')  # Valeur par défaut 0 si vide
                coef_value = request.POST.get(coef_key, '0')  # Valeur par défaut du coefficient = 1

                try:
                    note_value = float(note_value) if note_value else 0
                    coef_value = float(coef_value) if coef_value else 0
                except ValueError:
                    note_value = 0  # Si la conversion échoue, on met 0

                # Ajout de la note et du coefficient dans les données
                """notes_data[etudiant].append({
                    'note': note_value,
                    'coef': coef_value
                })"""
                if coef_value != 0:
                    notes_data[etudiant].append({
                        'note': note_value,
                        'coef': coef_value
                })
        # Trouver le nombre maximal de notes pour un étudiant
        max_notes_count = max(len(notes) for notes in notes_data.values())

        # Remplir les notes manquantes avec 0
        for etudiant, notes in notes_data.items():
            while len(notes) < max_notes_count:
                notes.append({'note': 0, 'coef': 0})  # Ajouter une note et un coefficient par défaut

        # Récupérer l'ID du module
        module_id = request.POST.get('module_id')

        # Traitez les données comme vous le faisiez dans votre code
        etudiants_modifies = []
        try:
            module = Cours_Module.objects.get(Id_module=module_id)
            nom_module = module.nom_module
            professeur = module.professeur
            professeurs = module.professeur.Id_prof
            administrateurs = Administration.objects.filter(is_superuser=True)
            filiere_id = module.filiere.Id_filiere  # Récupérer l'ID de la filière
            niveau = module.niveau  # Récupérer le niveau
        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('Professeur_dashboard')

        # Vérifier si des notes sont déjà enregistrées pour les étudiants dans ce module
        notes_existantes = {}
        for etudiant_matricule in etudiants:
            try:
                note = Notes.objects.get(
                    etudiant_id=etudiant_matricule,
                    matiere_module_id=module_id
                )
                notes_existantes[etudiant_matricule] = note
            except Notes.DoesNotExist:
                notes_existantes[etudiant_matricule] = None

        # Ajouter ou modifier les notes pour chaque étudiant
        for etudiant_matricule, notes in notes_data.items():
            note = notes_existantes.get(etudiant_matricule)
            
            if note:
                note.notes = notes  # Mettre à jour les notes si elles existent déjà
                note.save()
            else:
                # Si aucune note n'existe, créer une nouvelle entrée
                Notes.objects.create(
                    etudiant_id=etudiant_matricule,
                    matiere_module_id=module_id,
                    notes=notes
                )

            etudiant = Etudiant.objects.get(pk=etudiant_matricule)
            etudiants_modifies.append(etudiant.nom_etudiant)

        # Message de notification pour le professeur
        message = f"Des notes ont été ajoutées ou modifiées pour les étudiants suivants dans le module {nom_module} : {', '.join(etudiants_modifies)}."
        admin = administrateurs
        creer_notification(
            destinataire_prof=professeur,
            destinataire_admin=None,
            message=message
        )
        # Créer une notification pour chaque administrateur
        for admin in administrateurs:
            creer_notification(
                destinataire_admin=admin,  # Chaque administrateur est spécifié individuellement
                destinataire_prof=None,    # Aucun destinataire professeur pour cette notification
                message=message
            )

        messages.success(request, 'Les notes ont été enregistrées avec succès.')
        return redirect(reverse('liste_etudiants_par_classe', kwargs={'filiere_id': filiere_id, 'niveau': niveau, 'professeur_id': professeurs }))

    # Si c'est une requête GET, afficher le formulaire pour ajouter les notes

    if request.method == 'GET':
        filiere_id = request.GET.get('filiere_id')
        niveau = request.GET.get('niveau')
        module_id = request.GET.get('module_id')

        try:
            module = Cours_Module.objects.get(Id_module=module_id)
        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('Professeur_dashboard')

        # Vérifie si le professeur enseigne ce module
        if module.professeur.Id_prof != request.session.get('professeur_id'):
            messages.error(request, "Vous ne pouvez pas ajouter de notes pour ce module car vous ne l'enseignez pas.")
            return redirect('Professeur_dashboard')

        etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
        
        # Vérifie s'il existe déjà des moyennes pour ces étudiants dans ce module
        moyenne_existe = False
        for etudiant in etudiants:
            if Notes.objects.filter(etudiant=etudiant, matiere_module=module, moyenne__isnull=False).exists():
                moyenne_existe = True
                break  # Une seule suffit à bloquer

        if moyenne_existe:
            messages.error(request, "Des moyennes ont déjà été enregistrées pour ce module. Vous ne pouvez plus ajouter de notes.")
            #return redirect('Professeur_dashboard')
            #return redirect(reverse('liste_etudiants_par_classe', kwargs={'filiere_id': filiere_id, 'niveau': niveau, 'professeur_id': module.professeur.Id_prof }))
            return redirect(reverse('voir_notes_pro', kwargs={
                'filiere_id': filiere_id,
                'niveau': niveau
            }))


        # Si pas de moyenne, afficher le formulaire
        notes_map = {etudiant.matricule: etudiant.notes.all() for etudiant in etudiants}

        context = {
            'etudiants': etudiants,
            'module': module,
            'filiere_id': filiere_id,
            'niveau': niveau,
            'range_list': range(1, 6),
            'notes_existantes': notes_map
        }
        return render(request, 'prof/add_note_prof.html', context)

    return redirect(reverse('classe_pour_prof', kwargs={'filiere_id': filiere_id, 'niveau': niveau}))

def voir_notes_prof(request, filiere_id, niveau):
    if request.method == 'GET':
        module_id = request.GET.get('module_id')
        filiere_id = int(filiere_id)
        professeur_id = request.session.get('professeur_id')

        # Récupérer les modules enseignés par ce professeur dans cette filière
        modules = Cours_Module.objects.filter(filiere_id=filiere_id, professeur_id=professeur_id)

        module_selected = None
        notes = []
        max_notes = 0
        note_range = range(1, 1)
        coefficients = []

        if module_id:
            # Vérification que l'ID du module correspond bien à un seul module
            module_selected = get_object_or_404(Cours_Module, Id_module=int(module_id))

            # Récupérer tous les étudiants du niveau donné
            etudiants = Etudiant.objects.filter(niveau_etudiant=niveau)

            # Récupérer les notes existantes pour ce module
            notes_queryset = Notes.objects.filter(matiere_module=module_selected, etudiant__in=etudiants)

            # Désérialisation et traitement des notes
            notes_dict = {
                note.etudiant.matricule: {
                    'etudiant': note.etudiant,
                    'notes': json.loads(note.notes) if isinstance(note.notes, str) else note.notes,
                    'moyenne': note.moyenne,
                    'id': note.id,
                } for note in notes_queryset
            }
            for note in notes_queryset:
                #print(note.notes)  # Avant json.loads()

                # Désérialisation des notes si elles sont stockées en JSON
                notes_list = json.loads(note.notes) if isinstance(note.notes, str) else note.notes

                # Si notes_list est une liste de dictionnaires, nous extrayons les valeurs de 'note' et 'coef'
                if isinstance(notes_list, list) and all(isinstance(n, dict) for n in notes_list):
                    extracted_notes = [n.get('note') for n in notes_list if isinstance(n, dict)] if notes_list else []
                    extracted_coefs = [n.get('coef') for n in notes_list if isinstance(n, dict)] if notes_list else []
                else:
                    # Si notes_list contient des valeurs simples (par exemple des nombres), nous ajustons
                    extracted_notes = notes_list if notes_list else []
                    extracted_coefs = [1] * len(notes_list)  # Appliquer un coefficient de 1 si aucune info de coefficient

                notes_dict[note.etudiant.matricule] = {
                    'etudiant': note.etudiant,
                    'notes': extracted_notes,
                    'coefficients': extracted_coefs,  # On récupère les coefficients ici
                    'moyenne': note.moyenne,
                    'id': note.id,
                }


            # Vérifier quels étudiants n'ont pas de note et les ajouter à la liste
            for etudiant in etudiants:
                if etudiant.matricule not in notes_dict:
                    notes.append({
                        'etudiant': etudiant,
                        'notes': None,  # Aucun note enregistrée
                        'moyenne': 'Aucune note',
                        'id': None,
                    })
                else:
                    notes.append(notes_dict[etudiant.matricule])
                    max_notes = max(max_notes, len(notes_dict[etudiant.matricule]['notes']))

            note_range = range(1, max_notes + 1)
              # 🔹 Récupération des coefficients depuis la BD
             # Prendre les coefficients de n'importe quel étudiant ayant des notes
            for note_data in notes:
                if note_data['coefficients']:
                    coefficients = note_data['coefficients']
                    break  # On prend les coefficients d'un seul étudiant car ils sont censés être identiques


        context = {
            'modules': modules,
            'module_selected': module_selected,
            'notes': notes,
            'max_notes': max_notes,
            'note_range': note_range,
            'coefficients': coefficients,
            'niveau': niveau,
        }

        return render(request, 'prof/voir_notes_prof.html', context)
    else:
        return redirect('Professeur_dashboard')
    
def modifier_note_prof(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    
    if request.method == 'POST':
        notes_str = request.POST.getlist('notes')  # Récupère toutes les notes envoyées
        coefficients_str = request.POST.getlist('coefficients')  # Récupère les coefficients envoyés
        
        try:
            # Convertit les valeurs de notes et coefficients
            notes_float = [float(n.replace(',', '.')) if n else 0 for n in notes_str]
            coefficients_float = [float(c.replace(',', '.')) if c else 1 for c in coefficients_str]

            # Met à jour uniquement les notes modifiées sans écraser les autres
            updated_notes = []
            for i, (note_val, coef_val) in enumerate(zip(notes_float, coefficients_float)):
                if i < len(note.notes):  # Si l'index est dans les notes existantes
                    updated_notes.append({
                        'note': note_val if note_val != 0 else note.notes[i]['note'],  # Ne pas écraser la note si elle est déjà définie
                        'coef': coef_val if note_val != 0 else note.notes[i]['coef']  # Ne pas écraser le coefficient si la note est 0
                    })
                else:
                    updated_notes.append({
                        'note': note_val,
                        'coef': coef_val
                    })
            
            note.notes = updated_notes  # Met à jour la liste des notes sans écraser les anciennes
            note.save()

            filiere_id = note.matiere_module.filiere.Id_filiere
            niveau = note.matiere_module.niveau
            administrateurs = Administration.objects.all()

            # Envoyer des notifications aux administrateurs
            for admin in administrateurs:
                creer_notification(
                    destinataire_admin=admin,
                    message=f"Nouvelle note créée pour l'étudiant {note.etudiant}."
                )
            
            messages.success(request, 'Les notes ont été modifiées avec succès.')
            return redirect(reverse('voir_notes_pro', kwargs={'filiere_id': filiere_id, 'niveau': niveau}))

        except ValueError:
            messages.error(request, 'Veuillez saisir des nombres valides pour les notes.')
    
    # Récupération des coefficients des autres étudiants s'il n'y a pas de notes
    autres_notes = Notes.objects.exclude(id=note_id).values_list('notes', flat=True)
    coefficients_existants = []

    for notes_list in autres_notes:
        if isinstance(notes_list, list) and notes_list:
            coefficients_existants = [n['coef'] for n in notes_list if 'coef' in n]
            break  # Prendre le premier jeu de coefficients trouvé

    context = {
        'note': note,
        'coefficients_existants': coefficients_existants
    }
    return render(request, 'prof/modifier_note_prof.html', context)



def logout_prof(request):
    if 'professeur_id' in request.session:
        del request.session['professeur_id']  # Supprimer la session du professeur
    return redirect('connexion_Prof')  # Rediriger vers la page de connexion


# views.py
from django.shortcuts import render, get_object_or_404, redirect

from .forms import TacheForm

from django.contrib.auth.decorators import login_required


def ajouter_tache(request):
    if request.method == 'POST':
        form = TacheForm(request.POST)
        if form.is_valid():
            # Récupérer l'ID du professeur à partir de la session
            professeur_id = request.session.get('professeur_id')
            
            
            # Assurez-vous que l'ID du professeur existe dans la session
            if professeur_id:
                professeur = professeurs.objects.get(Id_prof=professeur_id)
                tache = form.save(commit=False)
                tache.professeur = professeur  # Associer la tâche au professeur
                tache.save()
                messages.success(request,"tache ajouté avec succès")
                return redirect('Professeur_dashboard')
            else:
                # Si le professeur n'est pas trouvé dans la session
                messages.success(request,"Reprenez")
                return redirect('Professeur_dashboard')  # Ou afficher un message d'erreur
    else:
        form = TacheForm()
    return render(request, 'prof/ajouter_tache.html', {'form': form})


def modifier_tache(request, id):
    tache = get_object_or_404(Tache, pk=id)
    
    # Vérifiez que la tâche appartient au professeur connecté
    if tache.professeur.Id_prof != request.session.get('professeur_id'):
        return redirect('Professeur_dashboard')  # Redirigez si ce n'est pas sa tâche
    
    if request.method == 'POST':
        form = TacheForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            messages.success(request,"tache modifié avec succès")
            return redirect('Professeur_dashboard')
    else:
        form = TacheForm(instance=tache)
    return render(request, 'prof/modifier_tache.html', {'form': form ,  'tache': tache})



def supprimer_tache(request, id):
    tache = get_object_or_404(Tache, id=id)
    
    # Vérifiez que la tâche appartient au professeur connecté
    if tache.professeur.Id_prof != request.session.get('professeur_id'):
        return redirect('Professeur_dashboard')  # Redirigez si ce n'est pas sa tâche
    
    if request.method == 'POST':
        tache.delete()
        return redirect('Professeur_dashboard')
     # Si ce n'est pas une requête POST, effectuer la suppression directement
    tache.delete()
    messages.success(request,"tache supprimé avec succès")
    return redirect('Professeur_dashboard')
        
    
    #return render(request, 'prof/supprimer_tache.html', {'tache': tache})

from django.http import JsonResponse


def get_taches(request):
    # Vérifiez si un professeur est connecté via la session
    if 'professeur_id' in request.session:
        professeur_id = request.session['professeur_id']
        
        # Récupérer le professeur en utilisant l'ID de la session
        try:
            professeur = professeurs.objects.get(Id_prof=professeur_id)
            
            # Filtrer les tâches pour ce professeur
            taches = Tache.objects.filter(professeur=professeur)
        except professeurs.DoesNotExist:
            taches = []  # Si le professeur n'existe pas, renvoyer une liste vide
    else:
        taches = []  # Si aucun professeur n'est connecté, renvoyer une liste vide

    # Préparer les données à renvoyer au frontend
    taches_data = [
        {
            'titre': tache.titre,
            'statut': tache.statut,
            'id': tache.id,
        }
        for tache in taches
    ]

    return JsonResponse({'taches': taches_data})

from Administration.views import creer_notification

def action_professeur(request, prof_id):
    professeur = get_object_or_404(professeurs, pk=prof_id)

    # Exemple d'une action : validation d'un devoir
    if request.method == 'POST':
        # Logique de validation
        creer_notification(
            destinataire_admin=None,  # Pas d'administrateur
            destinataire_prof=professeur,  # Destinataire : professeur
            evenement="Validation de devoir"
        )
        # Redirige après l'action
        return redirect('dashboard_professeur')
from Administration.models import Notifications

def notifications_professeur(request):
     # Récupérer l'ID du professeur à partir de la session
    professeur_id = request.session.get('professeur_id')

    if professeur_id:
        try:
            # Récupérer l'instance du professeur à partir de l'ID
            professeur = professeurs.objects.get(Id_prof=professeur_id)  # Ou le modèle qui correspond au professeur
        except Administration.DoesNotExist:
            messages.error(request, "Professeur non trouvé.")
            return redirect('Professeur_dashboard')  # Redirige vers une page d'accueil ou une page d'erreur
    else:
        messages.error(request, "Session invalide. Vous devez vous reconnecter.")
        return redirect('Professeur_dashboard')  # Redirige vers la page de connexion

    # Récupérer les notifications qui sont destinées au professeur
    notifications = Notifications.objects.filter(destinataire_prof=professeur).order_by('-date')
    notifications.filter(lu=False).update(lu=True)
    # Marquer les notifications comme lues si nécessaire
    #if 'mark_read' in request.GET:
     #   notification_ids = request.GET.getlist('mark_read')
     #   Notifications.objects.filter(id__in=notification_ids).update(lue=True)

    context = {
        'notifications': notifications,
        'notifications_non_lues': notifications.filter(lu=False).count(),
    }

    return render(request, 'prof/notifications.html', context)


def notifications_non_lues_count(request):
    try:
        # Récupérer l'ID du professeur dans la session
        
        professeur_id = request.session.get('professeur_id')
        
        # Vérifier si l'ID existe dans la session
        if not professeur_id:
            return JsonResponse({'error': 'ID professeur introuvable dans la session'}, status=400)

        # Vérifier que l'ID est valide
        notifications_non_lues = Notifications.objects.filter(
            destinataire_prof=professeur_id, lu=False
        ).count()

        # Retourner la réponse JSON avec le nombre de notifications non lues
        return JsonResponse({'notifications_non_lues': notifications_non_lues})

    except Exception as e:
        # Capturer toute erreur et retourner un message d'erreur
        return JsonResponse({'error': str(e)}, status=500)
    
from django.db.models import Prefetch
from Administration.models import professeurs
def profil(request ) :
    
    professeur_id = request.session.get('professeur_id')
    # Vérifier si l'ID est présent
    if not professeur_id:
        return redirect('connexion_Prof')  # Rediriger vers une page de connexion si non connecté

    # Récupérer le professeur correspondant ou afficher une erreur 404
    #professeur = get_object_or_404(professeurs, Id_prof=professeur_id)
    professeur = get_object_or_404(
        professeurs.objects.prefetch_related(
            Prefetch('cours_fichiers', queryset=CoursFichier.objects.select_related('module', 'filiere'))
        ), 
        Id_prof=professeur_id
    )
    modules = Cours_Module.objects.filter(professeur=professeur)
     # Calculer la somme du volume horaire
    total_volume_horaire = modules.aggregate(Sum('volume_horaire'))['volume_horaire__sum'] or 0

     # Calculer le nombre de filières enseignées
    nombre_filiere = modules.values('filiere').distinct().count()

    # Calculer le nombre de classes enseignées
    nombre_classes = modules.values('niveau').distinct().count()
    cours_historique = Cours_Module.objects.filter(professeur=professeur).order_by('-date_ajout')

     # Pourcentage des étudiants en fonction de leurs moyennes dans chaque module
    pourcentages_par_module = []
    for module in modules:
        notes_module = Notes.objects.filter(matiere_module=module)
        total_etudiants = notes_module.count()
        
        if total_etudiants > 0:
            pourcentage_par_moyenne = {
                'module': module.nom_module,
                'etudiants_10_plus': notes_module.filter(moyenne__gte=10).count() * 100 / total_etudiants,
                'etudiants_10_moins': notes_module.filter(moyenne__lt=10).count() * 100 / total_etudiants,
            }
            pourcentages_par_module.append(pourcentage_par_moyenne)
        
    # Ajouter ces informations dans le contexte
    
    

    context ={
        'professeur' : professeur,
        'modules': modules,
        'total_volume_horaire': total_volume_horaire,
        'nombre_filiere': nombre_filiere,
        'nombre_classes': nombre_classes,
        'pourcentages_par_module': pourcentages_par_module,
       
    }
    context['cours_historique'] = cours_historique
    context['pourcentages_par_moduleS'] = json.dumps(pourcentages_par_module)

    return render(request , 'prof/profil.html',context )
from datetime import date


from datetime import date  # Ajoutez ceci en haut de votre fichier


def appel_classe(request, filiere_id, niveau):
    professeur_id = request.session.get('professeur_id')
    

    if not professeur_id:
        return render(request, 'prof/appel.html', {'error_message': "Professeur non authentifié."})

    professeur = get_object_or_404(professeurs, Id_prof=professeur_id)

    

    if not filiere_id or not niveau:
        return render(request, 'prof/appel.html', {'error_message': "Tous les paramètres doivent être fournis."})

    modules = Cours_Module.objects.filter(filiere_id=filiere_id, professeur_id=professeur.Id_prof, niveau=niveau)

    if not modules.exists():
        return render(request, 'prof/appel.html', {'error_message': "Ce professeur n'enseigne pas dans cette filière."})

    etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
    form = AppelForm(request.POST or None,  professeur=professeur)

    form.fields['cours'].queryset = modules  # Filtrer les modules disponibles pour ce professeur

    if form.is_valid():
        cours_selectionne = form.cleaned_data['cours']
        date = form.cleaned_data['date']
        heure_debut = form.cleaned_data['heure_debut']
        heure_fin = form.cleaned_data['heure_fin']
        commentaire = form.cleaned_data['commentaire']

        for etudiant in etudiants:
            # Vérifier si un appel existe déjà pour cet étudiant, ce cours et cette date
            if Appel.objects.filter(etudiant=etudiant, cours=cours_selectionne, date=date).exists():
                continue  # Éviter la duplication

            
            present = f'present_{etudiant.matricule}' in request.POST and request.POST[f'present_{etudiant.matricule}'] == 'True'

            #present = True if present == "on" else False  # Boolean True/False

            # Enregistrer l'appel pour cet étudiant
            appel = Appel(
                etudiant=etudiant,
                cours=cours_selectionne,
                date=date,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                present=present,  # Boolean field
                commentaire=commentaire,
                professeur = professeur
            )
             # Debug: Vérifier quelles données sont envoyées

            appel.save()

        return redirect('voir_notes')


    context = {
        'modules': modules,
        'professeur': professeur,
        'etudiants': etudiants,
        'form': form,
        'filiere_id': filiere_id,
        'niveau': niveau,
        'date': timezone.now().date(),
    }

    return render(request, 'prof/Appel.html', context)








from collections import defaultdict

def listAppel(request, filiere_id, niveau):
    professeur_id = request.session.get('professeur_id')  
   
    professeur = get_object_or_404(professeurs, Id_prof=professeur_id)
    modules = Cours_Module.objects.filter(professeur=professeur)  # Récupérer les modules du professeur

    module_id = request.GET.get('module_id')  # Récupérer l'ID sélectionné dans le formulaire
    #print("Module ID récupéré :", module_id)  # Vérification

    appels = []
    etudiants = []
    dates_appels = []
    module = None
    presences = defaultdict(dict)  
    
    if module_id:  # Vérifier si un module a été sélectionné
        module = get_object_or_404(Cours_Module, Id_module=module_id, professeur=professeur)
        etudiants = Etudiant.objects.filter(filiere=module.filiere, niveau_etudiant=module.niveau)

        # Récupérer les appels pour ce module
        appels = Appel.objects.filter(cours=module).order_by('date')

        # Extraire les dates uniques des appels
        dates_appels = sorted(set(appels.values_list('date', flat=True)))
         # Remplir le dictionnaire des présences
        for appel in appels:
            presences[appel.etudiant.matricule][appel.date] = appel.present
    # Fonction pour récupérer la présence d'un étudiant à une date
     # Fonction pour récupérer la présence d'un étudiant à une date
    def get_presence(etudiant_id, date):
        try:
            # Recherche si un appel existe pour cet étudiant et cette date
            appel = Appel.objects.filter(etudiant__matricule=etudiant_id, date=date).first()
            if appel:
                return appel.present  # Retourne la présence (True ou False)
            return None  # Si pas d'appel trouvé, retourne None
        except Appel.DoesNotExist:
            return None
    context = {
        'professeur': professeur,
        'modules': modules,
        'etudiants': etudiants,
        'dates_appels': dates_appels,
        'filiere_id': filiere_id,
        'niveau' : niveau,
        'appels': appels,
        'module_id': module_id,  # Garder l'ID pour la sélection
        'module': module,  # Envoyer le module sélectionné
        'presences': presences,  # On envoie le dictionnaire des présences au template
        'get_presence': get_presence,  # Passer la fonction au template
    }
    return render(request, 'prof/listAppel.html', context)


#pour charger les infos des etudiants concernant l appel
def getAppelDetails(request):
    date = request.GET.get('date')
    appel = Appel.objects.filter(date=date).first()

    if appel:
        data = {
            "heure_debut": appel.heure_debut.strftime("%H:%M"),
            "heure_fin": appel.heure_fin.strftime("%H:%M"),
            "commentaire": appel.commentaire
        }
    else:
        data = {"error": "Aucun appel trouvé pour cette date."}

    return JsonResponse(data)


def disponibilite(request):
    professeur_id = request.session.get('professeur_id')

    # Récupération de tous les modules que ce professeur enseigne
    modules = Cours_Module.objects.filter(professeur_id=professeur_id)

    # Récupération des filières associées à ces modules
    filieres = Filiere.objects.all()

    # Récupération des niveaux associés à ces modules
    niveaux = Cours_Module.objects.filter(professeur_id=professeur_id).values('niveau').distinct()

    context = {
        'modules': modules,
        'filieres': filieres,
        'niveaux': niveaux,
        'erreur': None
    }

    if request.method == 'POST':
        module_id = request.POST.get('module')
        filiere_id = request.POST.get('filiere')
        niveau = request.POST.get('niveau')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        
        commentaire = request.POST.get('commentaire')

        if all([module_id, filiere_id, niveau, date_debut, date_fin]):
            # Vérifier si une disponibilité similaire existe déjà
            existe = Disponibilite.objects.filter(
                professeur_id=professeur_id,
                module_id=module_id,
                filiere_id=filiere_id,
                niveau=niveau
            ).exists()

            if existe:
                context['erreur'] = "Vous avez déjà renseigné une disponibilité pour ce module, filière et niveau."
            else:
                Disponibilite.objects.create(
                    professeur_id=professeur_id,
                    module_id=module_id,
                    filiere_id=filiere_id,
                    niveau=niveau,
                    date_debut=date_debut,
                    date_fin=date_fin,
                    commentaire=commentaire
                )
                return redirect('liste_disponibilites')
        else:
            context['erreur'] = "Tous les champs obligatoires doivent être remplis."

    return render(request, "prof/disponibilite.html", context)
###pour la recup 

import random
from faker import Faker
from django.http import JsonResponse
 # adapte selon l'import exact
from django.views.decorators.csrf import csrf_exempt

fake = Faker()

@csrf_exempt  # utile si tu veux tester sans csrf en POST aussi plus tard
def api_donnees_disponibilite(request):
    # 1. Génération aléatoire des modules
    modules = []
    for i in range(10):
        nom = fake.catch_phrase()
        niveau = random.choice([1, 2, 3])
        # Création en base
        module_obj = Cours_Module.objects.create(
            nom_module=nom,
            niveau=niveau,
            professeur_id=1  # ⚠️ à adapter, ou à rendre facultatif
        )
        modules.append({
            'Id_module': module_obj.Id_module,
            'nom_module': module_obj.nom_module,
            'niveau': module_obj.niveau
        })

    # 2. Génération aléatoire des filières
    filieres = []
    for i in range(7):
        nom = fake.job()
        filiere_obj = Filiere.objects.create(
            nom_filiere=nom
        )
        filieres.append({
            'Id_filiere': filiere_obj.Id_filiere,
            'nom_filiere': filiere_obj.nom_filiere
        })

    # 3. Niveaux distincts à partir des modules
    niveaux = list(set([mod['niveau'] for mod in modules]))

    return JsonResponse({
        'modules': modules,
        'filieres': filieres,
        'niveaux': niveaux
    })



import plotly.express as px
import pandas as pd
from django.utils.html import mark_safe
"""
def liste_disponibilites(request):
    filieres = Filiere.objects.all()
    niveau_filter = request.GET.get('niveau')
    filiere_filter = request.GET.get('filiere')

    disponibilites = Disponibilite.objects.all().select_related('professeur', 'module', 'filiere')
    
    # Appliquer le filtre uniquement si les deux valeurs sont renseignées
    if niveau_filter and filiere_filter:
        disponibilites = disponibilites.filter(niveau=niveau_filter, filiere_id=filiere_filter)
    else :
        erreur = "Aucune disponibilité trouvée pour les critères sélectionnés."



    niveaux = Etudiant._meta.get_field('niveau_etudiant').choices
    erreur = None
    if not disponibilites.exists():
        erreur = "Aucune disponibilité trouvée pour les critères sélectionnés."

    # Préparer les données pour le diagramme de Gantt
    data = []
    for dispo in disponibilites:
        data.append({
            'Enseignant': f"{dispo.professeur.nom_prof} ({dispo.module.nom_module})",
            'Start': dispo.date_debut,
            'Finish': dispo.date_fin,
        })

    df = pd.DataFrame(data)
    gantt_fig = px.timeline(df, x_start="Start", x_end="Finish", y="Enseignant", title="Disponibilités des enseignants")
    gantt_fig.update_yaxes(autorange="reversed")  # Pour que le premier enseignant soit en haut

    gantt_html = mark_safe(gantt_fig.to_html(full_html=False))

    context = {
        'disponibilites': disponibilites,
        'filieres': filieres,
        'niveaux': niveaux,
        'erreur': erreur,
        'gantt_graph': gantt_html,
    }

    return render(request, "prof/liste_disponibilites.html", context)

"""

def liste_disponibilites(request):
    filieres = Filiere.objects.all()
    niveaux = Etudiant._meta.get_field('niveau_etudiant').choices

    niveau_filter = request.GET.get('niveau')
    filiere_filter = request.GET.get('filiere')

    base_disponibilites = Disponibilite.objects.all().select_related('professeur', 'module', 'filiere')
    disponibilites = base_disponibilites  
  


    
    erreur = None
    gantt_html = None                   

    # Si les deux sont sélectionnés
    if niveau_filter and filiere_filter:
        disponibilites = base_disponibilites.filter(niveau=niveau_filter, filiere_id=filiere_filter)
        if not disponibilites.exists():
            erreur = "Aucune disponibilité trouvée pour les critères sélectionnés."
            disponibilites = Disponibilite.objects.none()
        else:
            # Générer graphique filtré
            gantt_html = build_gantt_chart(disponibilites)

    # Si un seul des deux est sélectionné
    elif niveau_filter or filiere_filter:
        if niveau_filter:
            disponibilites = base_disponibilites.filter(niveau=niveau_filter)
        if filiere_filter:
            disponibilites = disponibilites.filter(filiere_id=filiere_filter)
        gantt_html = build_gantt_chart(disponibilites)

    # Si aucun filtre n’est sélectionné
    else:
        disponibilites = base_disponibilites
        gantt_html = build_gantt_chart(disponibilites)

    context = {
        'disponibilites': disponibilites,
        'filieres': filieres,
        'niveaux': niveaux,
        'erreur': erreur,
        'gantt_graph': gantt_html,
        
    }

    return render(request, "prof/liste_disponibilites.html", context)

def build_gantt_chart(disponibilites):
    import pandas as pd
    import plotly.express as px
    from django.utils.safestring import mark_safe

    data = []
    for dispo in disponibilites:
        data.append({
            'Prof': f"{dispo.professeur.nom_prof} ({dispo.module.nom_module})",
            'VHG' : dispo.module.volume_horaire,
            'Start': dispo.date_debut,
            'Finish': dispo.date_fin,
           
        })

    if not data:
        return None

    df = pd.DataFrame(data)
    from datetime import timedelta

    df['color'] = 'Normal'

    # On suppose que les colonnes 'Start' et 'Finish' sont de type datetime
    prof_groups = df.groupby('Prof')

    for name, group in prof_groups:
        for idx1, row1 in group.iterrows():
            window_start = row1['Start'] - timedelta(days=3)
            window_end = row1['Finish'] + timedelta(days=3)
            
            for idx2, row2 in group.iterrows():
                if idx1 == idx2:
                    continue  # ne pas comparer un cours avec lui-même
                
                # Vérifier si l'autre cours tombe dans la fenêtre de ±3 jours
                if row2['Start'] <= window_end and row2['Finish'] >= window_start:
                    # Et vérifier s’il y a un chevauchement réel de temps
                    if row1['Start'] < row2['Finish'] and row2['Start'] < row1['Finish']:
                        df.loc[idx1, 'color'] = 'Chevauchement'
                        df.loc[idx2, 'color'] = 'Chevauchement'

        
 

    # Générer le Gantt avec couleurs
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Prof", color="color", title="Disponibilités des enseignants")
    fig.update_yaxes(autorange="reversed")

    return mark_safe(fig.to_html(full_html=False))


