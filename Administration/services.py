
from django.shortcuts import render, get_object_or_404, redirect
from .models import Etudiant, Notes, UploadedFile

class PersonnePrevenir:
    @staticmethod
    def get_etudiant_from_session(request):
        # Vérifier si la session contient l'ID de la personne à prévenir
        personne_prevenir_id = request.session.get('personne_prevenir_id')
        if not personne_prevenir_id:
            return None
        return get_object_or_404(Etudiant, matricule=personne_prevenir_id)

    @staticmethod
    def get_notes(etudiant):
        # Récupérer toutes les notes de l'étudiant
         # Récupérer toutes les notes de l'étudiant
        notes = Notes.objects.filter(etudiant=etudiant)
        
        # Créer une liste de dictionnaires avec les données à envoyer dans le template
        data = []
        for note in notes:
            data.append({
                'matiere': note.matiere_module.nom_module,  # Nom de la matière
                'note1': note.Note1,                       # Première note
                'note2': note.Note2,                       # Deuxième note
                'moyenne': note.moyenne                    # Moyenne des deux notes
            })
        
        return data

    @staticmethod
    def get_emploi_du_temps(etudiant):
        # Supposons que l'emploi du temps soit lié à l'étudiant
        
        return  UploadedFile.objects.filter(etudiant=etudiant)

    @staticmethod
    def get_uploaded_files(etudiant):
        # Récupérer les fichiers téléchargés
        return UploadedFile.objects.exclude(file__endswith='.xlsx').order_by('-uploaded_at')


