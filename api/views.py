from django.shortcuts import render, get_object_or_404


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


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

""""


class EtudiantNotesList(generics.ListAPIView):
    def get(self, request):
        # Assurez-vous que l'étudiant est connecté et qu'il a une session active
        etudiant_id = request.session.get('etudiant_id')
        if not etudiant_id:
            return Response({'error': 'Non authentifié'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            etudiant = Etudiant.objects.get(matricule=etudiant_id)
        except Etudiant.DoesNotExist:
            return Response({'error': 'Étudiant non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        etudiant_id = self.request.session.get('etudiant_id')
        if not etudiant_id:
            return Notes.objects.none()  # Aucun résultat si l'étudiant n'est pas authentifié

        return Notes.objects.filter(etudiant__matricule=etudiant_id)
  

"""


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
                'moyenne': note_data['moyenne']
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

        serializer = EtudiantSerializer(etudiant)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

#emploi du temps 

class UploadedFileListView(generics.ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
import pandas as pd

class UploadedFileDetailView(generics.RetrieveAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        file_path = file.file.path
        df = pd.read_excel(file_path)

        # Convert DataFrame to JSON
        data = df.to_dict(orient='records')

        return Response(data, status=status.HTTP_200_OK)
    
'''
def display_table(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)

    # Convertir DataFrame en HTML
    table_html = df.to_html(index=False)

    return Response({'table_html': table_html}, status=status.HTTP_200_OK)

'''
from rest_framework.decorators import api_view


@api_view(['GET'])
def display_table(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)

    # Convertir DataFrame en HTML
    table_html = df.to_html(index=False)

    return Response({'table_html': table_html}, status=status.HTTP_200_OK)


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