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

        return Response({
            'etudiant': etudiant_serializer.data,
            'notes': note_serializer.data
        }, status=status.HTTP_200_OK)


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