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
    print(f"filiere_id: {filiere_id}, professeur_id: {professeur.Id_prof}, niveau: {niveau}")
    modules = Cours_Module.objects.filter(filiere_id=filiere_id, professeur_id=professeur.Id_prof,niveau=niveau)
    #filiere = modules.first().filiere  # Récupérer la filière du premier module trouvé
    print(modules)
    filiere = getattr(modules.first(), 'filiere', None)
    print(filiere)
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

"""
def creer_note_prof(request):
    if request.method == 'GET':
        filiere_id = request.GET.get('filiere_id')
        niveau = request.GET.get('niveau')
        module_id = request.GET.get('module_id')
        etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)
        
        try:
            module = Cours_Module.objects.get(Id_module=module_id)
        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('Professeur_dashboard')  # Ou une autre page appropriée

        # Vérifie si le professeur enseigne ce module
        if module.professeur.Id_prof != request.session.get('professeur_id'):
            messages.error(request, "Vous ne pouvez pas ajouter de notes pour ce module car vous ne l'enseignez pas.")
            return redirect('Professeur_dashboard')

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
        
                # Utilisez une approche basée sur la structure dynamique des noms de champs
        

        



        etudiants_modifies = []

        try:
            # Récupérer le module pour obtenir son nom
            module = Cours_Module.objects.get(Id_module=module_id)
            nom_module = module.nom_module
            prof = module.professeur.nom_prof 
            prof_prenom = module.professeur.prenom_prof  # Récupérer le nom du professeur
        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('Professeur_dashboard')

        for etudiant_id, note1, note2 in zip(etudiants, notes1, notes2):
             # Vérification si les notes ne sont pas vides
            try:
                #note1 = float(note1) if note1 else None
                #note2 = float(note2) if note2 else None
                note1 = float(note1) if note1 else 0.0  # Convertir note1 en float, sinon mettre 0.0
                note2 = float(note2) if note2 else 0.0  # Convertir note2 en float, sinon mettre 0.0

                #print(f"Note1: {note1}, Note2: {note2}")

                if note1 is None and note2 is None:
                    continue  # Skip this entry if both notes are empty

                # Mise à jour ou création des notes
                
                note = Notes(
                        etudiant_id=etudiant_id, 
                        matiere_module_id=module_id, 
                        Note1=note1, 
                        Note2=note2
                    )
                    # Sauvegarde de la nouvelle note dans la base de données
                note.save()

                #print(f"Note créée ou mise à jour: {note}, créé: {created}")
                


                etudiant = Etudiant.objects.get(pk=etudiant_id)
                etudiants_modifies.append(etudiant.nom_etudiant)

            except ValueError:
                # Si les valeurs ne sont pas des nombres valides, on les ignore
                continue

        # Message de notification pour le professeur
        message = f"Des notes ont été ajoutées ou modifiées pour les étudiants suivants dans votre module {nom_module} : {', '.join(etudiants_modifies)}."
        creer_notification(
            destinataire_prof=module.professeur,
            message=message
        )

        messages.success(request, 'Les notes ont été enregistrées avec succès.')
        return redirect('Professeur_dashboard')

"""
from django.urls import reverse
#from .models import Administration
def creer_note_prof(request):
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
            professeurs = module.professeur.Id_prof
            administrateurs = Administration.objects.filter(is_superuser=True)
            filiere_id = module.filiere.Id_filiere  # Récupérer l'ID de la filière
            niveau = module.niveau  # Récupérer le niveau
        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('Professeur_dashboard')

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

        # Message de notification pour le professeur
        message = f"Des notes ont été ajoutées ou modifiées pour les étudiants suivants dans le  module {nom_module} : {', '.join(etudiants_modifies)}."
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
         # Rediriger vers 'liste_etudiants_par_classe' avec les paramètres appropriés
        return redirect(reverse('liste_etudiants_par_classe', kwargs={'filiere_id': filiere_id, 'niveau': niveau, 'professeur_id': professeurs }))

        #return redirect('Professeur_dashboard')

    # Si c'est une requête GET, afficher le formulaire pour ajouter les notes
    if request.method == 'GET':
        filiere_id = request.GET.get('filiere_id')
        niveau = request.GET.get('niveau')
        module_id = request.GET.get('module_id')
        etudiants = Etudiant.objects.filter(filiere_id=filiere_id, niveau_etudiant=niveau)

        try:
            module = Cours_Module.objects.get(Id_module=module_id)
        except Cours_Module.DoesNotExist:
            messages.error(request, "Le module spécifié n'existe pas.")
            return redirect('Professeur_dashboard')

        # Vérifie si le professeur enseigne ce module
        if module.professeur.Id_prof != request.session.get('professeur_id'):
            messages.error(request, "Vous ne pouvez pas ajouter de notes pour ce module car vous ne l'enseignez pas.")
            return redirect('Professeur_dashboard')

        context = {
            'etudiants': etudiants,
            'module': module,
            'filiere_id': filiere_id,
            'niveau': niveau,
            'range_list': range(1, 6)  # Exemple de la gamme de notes
        }
        return render(request, 'prof/add_note_prof.html', context)

    # Retourner une erreur si la méthode n'est ni GET ni POST
    return redirect('Professeur_dashboard')



"""
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
        return redirect('Professeur_dashboard')

"""


import json
def voir_notes_prof(request, filiere_id, niveau):
    if request.method == 'GET':
        module_id = request.GET.get('module_id')
        filiere_id = int(filiere_id)
        
        # Récupérer tous les modules pour cette filière
        modules = Cours_Module.objects.filter(filiere_id=filiere_id)
        
        # Initialiser les variables
        module_selected = None
        notes = None
        max_notes = 0  # Le nombre maximum de notes
        note_range = range(1, 1)  # Plage vide par défaut (ajustée plus tard)

        if module_id:
            module_selected = get_object_or_404(Cours_Module, Id_module=module_id)
            notes_queryset = Notes.objects.filter(matiere_module=module_selected,etudiant__niveau_etudiant=niveau)
            
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

        context = {
            'modules': modules,
            'module_selected': module_selected,
            'notes': notes,
            'max_notes': max_notes,
            'note_range': note_range,
            'niveau': niveau,
        }

        return render(request, 'prof/voir_notes_prof.html', context)
    else:
        return redirect('Professeur_dashboard')


def modifier_note_prof(request, note_id):
    """
    note = get_object_or_404(Notes, Id_note=note_id)
    
    if request.method == 'POST':
        note1_str = request.POST.get('note1', '')
        note2_str = request.POST.get('note2', '')
        
        try:
            note.Note1 = float(note1_str.replace(',', '.'))
            note.Note2 = float(note2_str.replace(',', '.'))
            note.save()
            administrateurs = Administration.objects.all()
            # Envoyer des notifications aux administrateurs
            for admin in administrateurs:
                creer_notification(
                    destinataire_admin=admin,
                    message=f"Nouvelle note créée pour l'étudiant {note.etudiant}."
                )
            messages.success(request, 'La note a été modifiée avec succès.')
            return redirect('Professeur_dashboard')
        except ValueError:
            messages.error(request, 'Veuillez saisir des nombres valides pour les notes.')
            # Gérer l'erreur ici, peut-être rediriger vers une page d'erreur ou afficher un message
    
    context = {
        'note': note
    }"""
    note = get_object_or_404(Notes, id=note_id)
    
    if request.method == 'POST':
        notes_str = request.POST.getlist('notes')  # Récupère toutes les notes envoyées
        
        try:
            notes_float = [float(n.replace(',', '.')) for n in notes_str]  # Convertit les valeurs
            note.notes = notes_float  # Met à jour la liste des notes
            note.save()
            administrateurs = Administration.objects.all()
            # Envoyer des notifications aux administrateurs
            for admin in administrateurs:
                creer_notification(
                    destinataire_admin=admin,
                    message=f"Nouvelle note créée pour l'étudiant {note.etudiant}."
                )
            
            messages.success(request, 'Les notes ont été modifiées avec succès.')
            return redirect('Professeur_dashboard')
        except ValueError:
            messages.error(request, 'Veuillez saisir des nombres valides pour les notes.')
    
    context = {
        'note': note
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
