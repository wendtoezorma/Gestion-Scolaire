from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import ScolariteSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

from .serializers import CoursFichierSerializer


# api/views.py

from rest_framework import viewsets
from Administration.models import Administration




class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer


# api/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Administration.models import Etudiant
from .serializers import EtudiantLoginSerializer, UpdatePasswordSerializer
"""
class EtudiantLoginView(APIView):
    def post(self, request):
        serializer = EtudiantLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            mot_de_passe = serializer.validated_data['mot_de_passe']
            try:
                etudiant = Etudiant.objects.get(email_etudiant=email)
                if etudiant.check_password(mot_de_passe):
                    if not etudiant.password_updated:
                        # Rediriger vers la mise à jour du mot de passe si ce n'est pas encore fait
                        return Response({'update_password_required': True, 'etudiant_id': etudiant.matricule}, status=status.HTTP_200_OK)
                    # Authentifier l'étudiant et créer une session
                    request.session['etudiant_id'] = etudiant.matricule
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            except Etudiant.DoesNotExist:
                return Response({'error': 'Email non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

class EtudiantLoginView(APIView):
    def post(self, request):
        serializer = EtudiantLoginSerializer(data=request.data)
        if serializer.is_valid():
            matricule = serializer.validated_data['matricule']
            mot_de_passe = serializer.validated_data['mot_de_passe']
            try:
                # Rechercher l'étudiant par matricule
                etudiant = Etudiant.objects.get(matricule=matricule)
                if etudiant.check_password(mot_de_passe):
                    if not etudiant.password_updated:
                        # Rediriger vers la mise à jour du mot de passe si ce n'est pas encore fait
                        return Response({'update_password_required': True, 'etudiant_id': etudiant.matricule}, status=status.HTTP_200_OK)
                    # Authentifier l'étudiant et créer une session
                    request.session['etudiant_id'] = etudiant.matricule
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Mot de passe incorrect'}, status=status.HTTP_400_BAD_REQUEST)
            except Etudiant.DoesNotExist:
                return Response({'error': 'Matricule non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    def post(self, request, etudiant_id):
        try:
            etudiant = Etudiant.objects.get(matricule=etudiant_id)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Etudiant non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            nouveau_mot_de_passe = serializer.validated_data['nouveau_mot_de_passe']
            etudiant.set_password(nouveau_mot_de_passe)  # Hash le nouveau mot de passe
            etudiant.password_updated = True  # Assurez-vous de mettre à jour ce champ si nécessaire
            etudiant.save()
            # Stocker l'identifiant de l'étudiant dans la session
            request.session['etudiant_id'] = etudiant.matricule
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EtudiantNotesList(APIView):
    def get(self, request):
        # Assurez-vous que l'étudiant est connecté et qu'il a une session active
        etudiant_id = request.session.get('etudiant_id')
        if not etudiant_id:
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            etudiant = Etudiant.objects.get(matricule=etudiant_id)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Étudiant non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer toutes les notes de l'étudiant
        notes = Notes.objects.filter(etudiant=etudiant)
        note_serializer = NotesSerializer(notes, many=True)
        etudiant_serializer = EtudiantSerializer(etudiant)
        
          # Organiser les notes en un dictionnaire
        notes_dict = {}
        for note_data in note_serializer.data:
            module_name = note_data['matiere_module']['nom_module']
            
            notes_dict[module_name] = {
                'Note1': note_data['Note1'],
                'Note2': note_data['Note2'],
                'moyenne': note_data['moyenne'],
                
            }

        return Response({
            'etudiant': etudiant_serializer.data,
            'notes': notes_dict
        }, status=status.HTTP_200_OK)
        
        '''return Response({
            'etudiant': etudiant_serializer.data,
            'notes': note_serializer.data
        }, status=status.HTTP_200_OK)'''


class ModulesClasseView(APIView):
    def get(self, request):
        # Assurez-vous que l'étudiant est connecté et qu'il a une session active
        etudiant_id = request.session.get('etudiant_id')
        if not etudiant_id:
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            etudiant = Etudiant.objects.get(matricule=etudiant_id)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Étudiant non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer tous les modules de la filière de l'étudiant
        modules = Cours_Module.objects.filter(filiere=etudiant.filiere)
        module_serializer = CoursModuleSerializer(modules, many=True)
        etudiant_serializer = EtudiantSerializer(etudiant)

        return Response({
            'etudiant': etudiant_serializer.data,
            'modules': module_serializer.data
        }, status=status.HTTP_200_OK)

class StudentProfileView(APIView):
    def get(self, request):
        # Récupère l'étudiant connecté à partir de la session
        etudiant_id = request.session.get('etudiant_id')
        if not etudiant_id:
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            etudiant = Etudiant.objects.get(matricule=etudiant_id)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Étudiant non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EtudiantSerializer(etudiant, context={'request': request})
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
#emploi du temps 

class UploadedFileListView(generics.ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
import pandas as pd
"""
class UploadedFileDetailView(generics.RetrieveAPIView):
    queryset = UploadedFile.objects.all()
    
    
    serializer_class = UploadedFileSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        file_path = file.file.path
        df = pd.read_excel(file_path)

         # Remplacer les valeurs NaN par None (qui est JSON-compatible)
        df = df.fillna('')
        # Convert DataFrame to JSON
        data = df.to_dict(orient='records')

        return Response(data, status=status.HTTP_200_OK)
    
"""
import pandas as pd
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import UploadedFileSerializer
from django.template.loader import render_to_string

class UploadedFileDetailView(generics.RetrieveAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        # Récupérer le fichier correspondant à l'ID
        file = self.get_object()
        file_path = file.file.path  # Obtenir le chemin du fichier
        df = pd.read_excel(file_path)  # Lire le fichier Excel avec pandas

        # Remplacer les valeurs NaN par une chaîne vide
        df = df.fillna('')

        # Convertir les données en HTML
        html_table = self.convert_to_html_table(df)

        # Retourner le tableau HTML comme réponse
        return Response({"html_table": html_table}, status=status.HTTP_200_OK)

    def convert_to_html_table(self, df):
        # Convertir le DataFrame en tableau HTML
        html = df.to_html(index=False, classes="table table-striped table-bordered")
        return html
    

from rest_framework.decorators import api_view


import pandas as pd
import pdfplumber
from rest_framework.decorators import api_view
from django.http import JsonResponse

from django.shortcuts import get_object_or_404
from rest_framework import status
import os

import io
import pandas as pd
import pdfplumber
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import pandas as pd
import io
import pdfplumber


class DisplayTableAPIView(APIView):
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    def get(self, request, file_id):
        # Récupérer le fichier correspondant à l'ID dans la base de données
        uploaded_file = get_object_or_404(UploadedFile, id=file_id)
        
        # Récupérer le contenu du fichier depuis la base de données
        file_content = uploaded_file.file.read()

        # Vérifier la taille du fichier
        if len(file_content) > self.MAX_FILE_SIZE:
            return Response({'error': 'File is too large'}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier l'extension du fichier
        file_extension = uploaded_file.file.name.split('.')[-1].lower()

        # Si c'est un fichier Excel
        if file_extension in ['xls', 'xlsx']:
            try:
                # Lire le fichier Excel dans un DataFrame pandas
                df = pd.read_excel(io.BytesIO(file_content))

                 # Nettoyer les NaN dans le DataFrame (remplacer les NaN par des chaînes vides)
                df.fillna("", inplace=True)

                # Supprimer les colonnes vides (entièrement vides)
                df.dropna(axis=1, how='all', inplace=True)

                # Supprimer les lignes vides (lignes qui ont seulement des valeurs vides)
                df.dropna(axis=0, how='all', inplace=True)
                df.fillna("", inplace=True)
                data = df.to_dict(orient='records')
                return Response({'data': data}, status=status.HTTP_200_OK)
            except pd.errors.ParserError as e:
                return Response({'error': f'Error parsing Excel file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'Erreur lors de la lecture du fichier Excel: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si c'est un fichier PDF
        elif file_extension == 'pdf':
            try:
                # Lire le fichier PDF avec pdfplumber
                with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text()
                return Response({'data': text}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Erreur lors de la lecture du fichier PDF: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Si le format de fichier n'est pas supporté
        else:
            return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)


"""
@api_view(['GET'])
def display_table(request, file_id):
    
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    
    # Vérifier l'extension du fichier
    file_extension = os.path.splitext(file_path)[1].lower()
      
      # Lire le fichier en tant que fichier binaire

    file_content = uploaded_file.file.read()

    if file_extension in ['.xls', '.xlsx']:  # Si c'est un fichier Excel
        # Lire le fichier Excel dans un DataFrame pandas
        #df = pd.read_excel(file_path)
        df = pd.read_excel(io.BytesIO(file_content), engine='openpyxl')

        # Convertir le DataFrame en dictionnaire
        data = df.to_dict(orient='records')
        return JsonResponse({'data': data}, status=status.HTTP_200_OK)
    
    elif file_extension == '.pdf':  # Si c'est un fichier PDF
        # Lire le fichier PDF avec pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return JsonResponse({'data': text}, status=status.HTTP_200_OK)
    
    else:
        return JsonResponse({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import pandas as pd
from Administration.models import UploadedFile

def download_pdf(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)

    # Remplacer les NaN par des chaînes vides
    df.fillna('', inplace=True)

    # Créer un buffer pour sauvegarder le PDF
    buffer = BytesIO()
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
    response['Content-Disposition'] = 'attachment; filename="emploi_du_temps.pdf"'

    return response
"""



from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pandas as pd
from io import BytesIO
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
"""
def download_pdf(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)

    # Remplacer les NaN par des chaînes vides
    df.fillna('', inplace=True)

    # Créer un buffer pour sauvegarder le PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Préparer les données pour le tableau
    data = [df.columns.to_list()] + df.values.tolist()

    # Créer le tableau
    table = Table(data)

    # Appliquer un style au tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # En-tête en gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texte blanc dans l'en-tête
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrer le texte dans les cellules
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Police en gras pour l'en-tête
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espacement en bas des cellules d'en-tête
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fond beige pour le reste du tableau
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grille autour du tableau
    ])
    table.setStyle(style)

    # Ajuster la largeur des colonnes (si nécessaire)
    column_widths = [max(len(str(item)) for item in col) * 7 for col in zip(*data)]  # ajuster la largeur en fonction du contenu
    table._argW = column_widths  # Appliquer les largeurs calculées aux colonnes

    # Construire le PDF
    elements = []
    elements.append(table)
    doc.build(elements)

    # Créer une réponse HTTP avec le contenu du PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="emploi_du_temps.pdf"'

    return response

"""
import os
import shutil
import xlwings as xw
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
  # Assurez-vous que vous avez un modèle UploadedFile
import os
import shutil
import xlwings as xw
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
import tempfile
def download_pdf(request, file_id):
    """
    Télécharge directement le fichier PDF spécifié par son ID.
    """
    # Récupération du fichier correspondant à l'ID
    file_instance = get_object_or_404(UploadedFile, id=file_id)
    
    # Renvoie le fichier comme réponse avec l'en-tête pour le téléchargement
    response = FileResponse(file_instance.file.open('rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_instance.file.name}"'
    return response

class CoursFichierAPIs(APIView):
    def get(self, request):
        cours_fichiers = CoursFichier.objects.all()
        serializer = CoursFichierSerializer(cours_fichiers, many=True)

        # Générer le contenu HTML avec des liens téléchargeables
        html_content = """
        <html>
        <head><title>Liste des fichiers</title></head>
        <body>
        <h1>Liste des fichiers de cours</h1>
        <ul>
        """
        for fichier in serializer.data:
            #fichier_url = fichier['fichier']
            fichier_url = request.build_absolute_uri(fichier['fichier'])  # Django gère déjà les URLs complètes pour les fichiers
            html_content += f"""
            <li>
                <strong>Nom fichier :</strong> {fichier['nom_fichier']}<br>
                <strong>Fichier :</strong> <a href="{fichier_url}" download="{fichier['nom_fichier']}">Télécharger</a><br>
                <strong>Date ajout :</strong> {fichier['date_ajout']}<br>
                <strong>Professeur :</strong> {fichier['professeur']}<br>
                <strong>Module :</strong> {fichier['module']}<br>
                <strong>Filière :</strong> {fichier['filiere']}<br>
                <strong>Niveau :</strong> {fichier['niveau']}<br>
                <strong>Année académique :</strong> {fichier['annee_academique_cour']}<br>
                <strong>Type de fichier :</strong> {fichier['type_fichier']}
            </li><br><br>
            """
        html_content += "</ul></body></html>"

        return Response(html_content, content_type="text/html", status=status.HTTP_200_OK)
    


class CoursFichierAPI(APIView):
    def get(self, request):
        cours_fichiers = CoursFichier.objects.all()
        serializer = CoursFichierSerializer(cours_fichiers, many=True)

        # Générer le contenu JSON avec des liens téléchargeables
        data = []
        for fichier in serializer.data:
            download_url = request.build_absolute_uri(
                reverse('download_pdf', args=[fichier['id_fichier']])
            )
            fichier_info = {
                'Id_fichier': fichier['id_fichier'],
                'nom_fichier': fichier['nom_fichier'],
                'fichier': download_url,
                'date_ajout': fichier['date_ajout'],
                'professeur': fichier['nom_professeur'],
                'module': fichier['nom_module'],
                'filiere': fichier['nom_filiere'],
                'niveau': fichier['niveau'],
                'annee_academique': fichier['annee_academique_cour'],
                'type_fichier': fichier['type_fichier'],
            }
            data.append(fichier_info)

        return Response(data, status=status.HTTP_200_OK)






from django.http import HttpResponse, Http404, FileResponse
def download_pdf_cours(request, file_id):
  # Récupérer le fichier correspondant à l'ID
    cours_fichier = get_object_or_404(CoursFichier, id_fichier=file_id)

    # Obtenir le chemin du fichier PDF (dans ce cas, 'fichier' est supposé être un champ FileField)
    file_path = cours_fichier.fichier.path  # Obtenir le chemin complet du fichier sur le serveur

    try:
        # Ouvrir le fichier PDF et préparer une réponse FileResponse pour permettre le téléchargement
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        # Si le fichier est introuvable
        raise Http404("Le fichier demandé n'existe pas ou a été supprimé.")

    # Facultatif : vous pouvez ajouter une disposition de téléchargement si vous voulez que le fichier soit téléchargé automatiquement
    response['Content-Disposition'] = f'attachment; filename="{cours_fichier.nom_fichier}.pdf"'

    return response

class ScolariteDetailView(APIView):
    def get(self, request):
        etudiant_id = request.session.get('etudiant_id')
        if not etudiant_id:
            return Response({"error": "Non authentifié"}, status=401)

        # Récupérer l'étudiant
        etudiant = get_object_or_404(Etudiant, matricule=etudiant_id)
        
        # Récupérer la scolarité de cet étudiant
        scolarite = Scolarite.objects.filter(etudiant=etudiant).first()
        
        if scolarite:
            serializer = ScolariteSerializer(scolarite)
            return Response(serializer.data)  # DRF renvoie automatiquement en JSON
        
        return Response({"message": "Aucune donnée de scolarité trouvée"}, status=404)
    


class InfosView(APIView):
    def get(self, request):
        # Vérifier si l'utilisateur est authentifié
        if not request.session.get('etudiant_id'):
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)

        # Récupérer toutes les informations
        infos_list = Infos.objects.all()

        if not infos_list.exists():
            return Response({'message': 'Aucune information trouvée'}, status=status.HTTP_404_NOT_FOUND)

        # Construire l'URL complète pour chaque fichier
        infos_with_full_path = []
        for info in infos_list:
            data = {
                'id_infos': info.id_infos,
                'titre': info.titre,
                'message': info.message,
                'contenu': request.build_absolute_uri(info.contenu.url) if info.contenu else None,
                'date_creation': info.date_creation
            }
            infos_with_full_path.append(data)

        return Response(infos_with_full_path, status=status.HTTP_200_OK)

    def post(self, request):
        # Vérifier si l'utilisateur est authentifié
        if not request.session.get('etudiant_id'):
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)

        # Inclure request.FILES pour gérer les fichiers téléchargés
        serializer = InfosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

import requests

def verifier_etudiants_connectes(request):
    """
    Vérifie l'état de connexion de chaque étudiant en interrogeant l'application mobile.
    """
    mobile_api_url = "http://localhost:3001/is-connected/"
    etudiants = Etudiant.objects.all()

    connectes = 0
    for etudiant in etudiants:
        try:
            response = requests.get(f"{mobile_api_url}{etudiant.matricule}")
            if response.status_code == 200 and response.json().get("connected"):
                etudiant.Connecter = True
                connectes += 1
            else:
                etudiant.Connecter = False
            etudiant.save()
        except requests.ConnectionError:
            return JsonResponse({"success": False, "message": "Erreur de connexion à l'application mobile."}, status=500)

    return JsonResponse({"success": True, "connectes": connectes})

from rest_framework.exceptions import NotFound

class ConnexionPersonnePrevenir(APIView):
    def post(self, request):
        numero = request.data.get('numero_personne_prevenir')
        nom = request.data.get('nom_personne_prevenir')
        try:
            etudiant = Etudiant.objects.get(nom_personne_prevenir=nom, numero_personne_prevenir=numero)
            request.session['personne_prevenir_id'] = etudiant.matricule
            return Response({"message": "Connexion réussie", "etudiant": EtudiantSerializer(etudiant).data})
        except Etudiant.DoesNotExist:
            raise NotFound("Nom ou numéro invalide.")

class DeconnexionPersonnePrevenir(APIView):
    def post(self, request):
        if 'personne_prevenir_id' in request.session:
            del request.session['personne_prevenir_id']
        return Response({"message": "Déconnexion réussie"})

class DashboardPersonnePrevenir(APIView):
    def get(self, request):
        personne_prevenir_id = request.session.get('personne_prevenir_id')
        if not personne_prevenir_id:
            return Response({"error": "Vous n'êtes pas autorisé à accéder à cette page."}, status=403)
        
        try:
            etudiant = Etudiant.objects.get(matricule=personne_prevenir_id)
            return Response(EtudiantSerializer(etudiant).data)
        except Etudiant.DoesNotExist:
            raise NotFound("Aucune donnée trouvée.")

class PersonnePrevenirAction(APIView):
    def get(self, request, action_type):
        personne_prevenir_id = request.session.get('personne_prevenir_id')
        if not personne_prevenir_id:
            return Response({"error": "Vous devez être connecté."}, status=401)
        
        try:
            etudiant = Etudiant.objects.get(matricule=personne_prevenir_id)
        except Etudiant.DoesNotExist:
            raise NotFound("Etudiant non trouvé.")
        
        if action_type == 'notes':
            notes = Notes.objects.filter(etudiant=etudiant)
            data = NotesSerializer(notes, many=True).data
            return Response(data)
        
        elif action_type == 'emploi_du_temps':
            files = UploadedFile.objects.filter(etudiant=etudiant)
            data = UploadedFileSerializer(files, many=True).data
            return Response(data)
        
        elif action_type == 'uploaded_files':
            files = UploadedFile.objects.exclude(file__endswith='.xlsx').order_by('-uploaded_at')
            data = UploadedFileSerializer(files, many=True).data
            return Response(data)
        
        else:
            return Response({"error": "Action non valide."}, status=400)
        
class ParentInfoApi(APIView):
    def get(self, request):
        # Vérifier si l'utilisateur est authentifié
        if not request.session.get('personne_prevenir_id'):
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)

        # Récupérer toutes les informations
        infos_list = Infos.objects.all()

        if not infos_list.exists():
            return Response({'message': 'Aucune information trouvée'}, status=status.HTTP_404_NOT_FOUND)

        # Construire l'URL complète pour chaque fichier
        infos_with_full_path = []
        for info in infos_list:
            data = {
                'id_infos': info.id_infos,
                'titre': info.titre,
                'message': info.message,
                'contenu': request.build_absolute_uri(info.contenu.url) if info.contenu else None,
                'date_creation': info.date_creation
            }
            infos_with_full_path.append(data)

        return Response(infos_with_full_path, status=status.HTTP_200_OK)
    
class ParentScolariteDetailView(APIView):
    def get(self, request):
        # Vérifier si l'utilisateur est authentifié
        if not request.session.get('personne_prevenir_id'):
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def get(self, request):
        # Récupérer l'ID de l'étudiant depuis la session
        personne_prevenir_id = request.session.get('personne_prevenir_id')
        
        # Vérifier si l'ID de l'étudiant existe dans la session
        if not personne_prevenir_id :
            return Response({"error": "Non authentifié"}, status=401)
        
        # Récupérer l'étudiant correspondant à l'ID depuis la base de données
        etudiant = get_object_or_404(Etudiant, matricule=personne_prevenir_id)
        
        # Récupérer la scolarité de cet étudiant
        scolarite = Scolarite.objects.filter(etudiant=etudiant).first()
        
        # Si des données de scolarité existent pour cet étudiant, les sérialiser et renvoyer
        if scolarite:
            serializer = ScolariteSerializer(scolarite)
            print("Données de scolarité : ", serializer.data)
            return Response(serializer.data)  # DRF renvoie automatiquement les données en JSON
        
        # Si aucune scolarité n'est trouvée pour cet étudiant
        return Response({"message": "Aucune donnée de scolarité trouvée"}, status=404)
    

