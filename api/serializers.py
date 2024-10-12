# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from Administration.models import *



class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = '__all__'

class CoursModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours_Module
        fields = ['nom_module']

class EtudiantLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True)

class UpdatePasswordSerializer(serializers.Serializer):
    nouveau_mot_de_passe = serializers.CharField(write_only=True)

class NotesSerializer(serializers.ModelSerializer):
    matiere_module = CoursModuleSerializer()
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
        fields = ['matricule', 'nom_etudiant', 'prenom_etudiant', 'email_etudiant', 'telephone_etudiant', 'sexe_etudiant', 'Date_naiss_etudiant', 'lieu_naiss_etudiant', 'nationalite_etudiant', 'niveau_etudiant', 'annee_academique_etudiant', 'filiere','photo']


#emploi du temps 

class UploadedFileSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at', 'view_url','download_url']
    def get_download_url(self, obj):
        request = self.context.get('request')
        download_url = request.build_absolute_uri(f'/emploi_du_temps/{obj.id}/download/')
        return download_url
    
    def get_view_url(self, obj):
        request = self.context.get('request')
        view_url = request.build_absolute_uri(f'/emploi_du_temps/{obj.id}/view/')
        return view_url
    

class CoursFichierSerializer(serializers.ModelSerializer):
    nom_professeur = serializers.CharField(source='professeur.nom_prof', read_only=True)
    nom_module = serializers.CharField(source='module.nom_module',read_only=True)
    nom_filiere = serializers.CharField(source='filiere.nom_filiere',read_only=True)
    class Meta:
        model = CoursFichier
        fields = '__all__'

class ScolariteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scolarite
        fields = ['tranche_1', 'tranche_2', 'tranche_3', 'montant_total_verse', 'Montant_restant', 'date_payement']


class InfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infos
        fields = ['id_infos', 'titre', 'message', 'contenu', 'date_creation']