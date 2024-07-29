# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from Administration.models import *



class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = '__all__'



class EtudiantLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True)

class UpdatePasswordSerializer(serializers.Serializer):
    nouveau_mot_de_passe = serializers.CharField(write_only=True)

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['matiere_module', 'Note1', 'Note2', 'moyenne']




class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = ['nom_filiere']

class CoursModuleSerializer(serializers.ModelSerializer):
    filiere = FiliereSerializer()  # Utilisez le serializer de Filiere

    class Meta:
        model = Cours_Module
        fields = ['nom_module', 'credit_module', 'volume_horaire','filiere']

class EtudiantSerializer(serializers.ModelSerializer):
    filiere = FiliereSerializer()
    class Meta:
        model = Etudiant
        fields = ['matricule', 'nom_etudiant', 'prenom_etudiant', 'email_etudiant', 'telephone_etudiant', 'sexe_etudiant', 'Date_naiss_etudiant', 'lieu_naiss_etudiant', 'nationalite_etudiant', 'niveau_etudiant', 'annee_academique_etudiant', 'filiere']


