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
    matricule = serializers.CharField(max_length=200)
    # email = serializers.EmailField()
    mot_de_passe = serializers.CharField(write_only=True)

class UpdatePasswordSerializer(serializers.Serializer):
    nouveau_mot_de_passe = serializers.CharField(write_only=True)
'''
class NotesSerializer(serializers.ModelSerializer):
    
    matiere_module = CoursModuleSerializer()
    class Meta:
        model = Notes
        fields = ['Note1', 'Note2', 'moyenne','nom_professeur']
'''
class NotesSerializer(serializers.ModelSerializer):
    matiere_module = CoursModuleSerializer()
    class Meta:
        model = Notes
        fields = ['matiere_module', 'Note1', 'Note2', 'moyenne']



class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = ['nom_filiere']
class ProfesseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = professeurs
        fields = ['nom_prof', 'prenom_prof']  # Vous pouvez ajouter d'autres champs si nécessaire


class CoursModuleSerializer(serializers.ModelSerializer):
    filiere = FiliereSerializer()  # Utilisez le serializer de Filiere
    professeur = ProfesseurSerializer()
    class Meta:
        model = Cours_Module
        fields = ['Id_module','nom_module', 'credit_module', 'volume_horaire','filiere','professeur']

class EtudiantSerializer(serializers.ModelSerializer):
    filiere = FiliereSerializer()
    class Meta:
        model = Etudiant
        fields = ['matricule', 'nom_etudiant', 'prenom_etudiant', 'email_etudiant', 'telephone_etudiant', 'sexe_etudiant', 'Date_naiss_etudiant', 'lieu_naiss_etudiant', 'nationalite_etudiant', 'niveau_etudiant', 'annee_academique_etudiant', 'filiere','photo','chef_de_classe',]

   
    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo:
            photo_url = obj.photo.url
            return request.build_absolute_uri(photo_url)
        return None  # ou return '' si vous préférez une chaîne vide

#emploi du temps 

class UploadedFileSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    class Meta:
        model = UploadedFile
        fields = '__all__' #['id', 'file', 'uploaded_at', 'view_url','download_url']
    def get_download_url(self, obj):
        request = self.context.get('request')
        download_url = request.build_absolute_uri(f'/api/emploi_du_temps/{obj.id}/download/')
        return download_url
    
    def get_view_url(self, obj):
        request = self.context.get('request')
        view_url = request.build_absolute_uri(f'/api/emploi_du_temps/{obj.id}/view/')
        return view_url
    

class CoursFichierSerializer(serializers.ModelSerializer):
    #Id_fichier = serializers.AutoField
    nom_professeur = serializers.CharField(source='professeur.nom_prof', read_only=True)
    nom_module = serializers.CharField(source='module.nom_module',read_only=True)
    nom_filiere = serializers.CharField(source='filiere.nom_filiere',read_only=True)
    class Meta:
        model = CoursFichier
        fields = '__all__'

class BoursierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boursier
        fields = ['id', 'type_bourse', 'reduction']


class ScolariteSerializer(serializers.ModelSerializer):
    bourse = serializers.CharField(source='etudiant.bourse')
    tranches = serializers.SerializerMethodField()

    class Meta:
        model = Scolarite
        fields = ['tranches', 'montant_total_verse', 'Montant_restant', 'date_payement','bourse','total']

    def get_tranches(self, obj):
        # Vérifie que obj.tranches est une liste et filtre les valeurs > 0
        if isinstance(obj.tranches, list):
            return [tranche for tranche in obj.tranches if tranche > 0]
        return []


class InfosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infos
        fields = ['id_infos', 'titre', 'message', 'contenu', 'date_creation']

#pour les parents

class NotesSerializer(serializers.ModelSerializer):
    nom_module = serializers.SerializerMethodField()
    professeur_nom = serializers.SerializerMethodField()  # Nouveau champ pour récupérer le nom du professeur
    notes_details = serializers.SerializerMethodField()
    credit_module = serializers.SerializerMethodField()
    semestre = serializers.SerializerMethodField()
    moyenne = serializers.SerializerMethodField()

    class Meta:
        model = Notes
        fields = ['nom_module',  'moyenne','professeur_nom','notes_details','credit_module','semestre']  # Ajoutez d'autres champs si nécessaire

    def get_nom_module(self, obj):
        # Récupérer le nom du module à partir de la relation (ForeignKey)
        return obj.matiere_module.nom_module
    
    def get_professeur_nom(self, obj):
        # Récupérer le nom complet du professeur lié au module
        return obj.matiere_module.professeur.get_nom_prof()  # Utiliser la méthode pour obtenir le nom complet du professeur
    
    def get_credit_module(self, obj):
        # Récupérer le coef lié au module
        return obj.matiere_module.credit_module  # Utiliser la méthode pour obtenir le nom complet du professeur
    
    
    def get_semestre(self, obj):
        # Récupérer le nom complet du professeur lié au module
        return obj.matiere_module.semestre
    
    def get_notes_details(self, obj):
        # Ici, vous retournez les notes détaillées, si vous le souhaitez
        notes_details = {}
        for i, note in enumerate(obj.notes):
            note_key = f"Note{i + 1}"  # Note1, Note2, Note3, ...
            notes_details[note_key] = note
        return notes_details
          # Vous pouvez ajuster la logique ici si nécessaire
    def get_moyenne(self, obj):
        return round(obj.moyenne, 2)  # Limite à 2 décimales


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'uploaded_at']  # Ajoutez d'autres champs si nécessaire

from rest_framework import serializers

from rest_framework import serializers


import re 

def extract_volume_as_int(volume_horaire):
    match = re.match(r"(\d+)", volume_horaire)  # Capture tous les chiffres au début
    return int(match.group(1)) if match else 0  # Convertir en entier si trouvé, sinon 0

from rest_framework import serializers

"""

class AvancementCoursSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.CharField(source='etudiant.nom_etudiant', read_only=True)
    images = ImageSerializer(many=True)
    class Meta:
        model = AvancementCours
        fields = [
            'id', 'etudiant_nom', 'cours_module', 'volume_horaire_total','volume_horaire_restant',
            'volume_horaire_realise', 'pourcentage_avancement','heure_debut','heure_fin','images', 'date_op'
        ]
        read_only_fields = ['etudiant', 'cours_module', 'pourcentage_avancement', 'date_op', 'volume_horaire_total','volume_horaire_restant']



    @staticmethod
    def calculate_volume_horaire_restant(etudiant, cours_module, volume_horaire_realise):
        
        # Vérifier si c'est le premier enregistrement pour cet étudiant et ce module
        if not AvancementCours.objects.filter(etudiant=etudiant, cours_module=cours_module).exists():
            # Si c'est le premier enregistrement, initialiser volume_horaire_restant avec volume_horaire_total
            return extract_volume_as_int(cours_module.volume_horaire) - volume_horaire_realise

        else:
            # Chercher l'avancement précédent de l'étudiant pour ce module là
            avancement_precedent = AvancementCours.objects.filter(
                etudiant=etudiant,
                cours_module=cours_module
            ).order_by('-date_op').first()  # Prendre le plus récent

            if avancement_precedent:
                # Calculer le volume horaire restant basé sur l'enregistrement précédent
                return avancement_precedent.volume_horaire_restant - volume_horaire_realise
            else:
                # Si aucun avancement précédent, calculer à partir du volume horaire total du module
                return extract_volume_as_int(cours_module.volume_horaire) - volume_horaire_realise

    def create(self, validated_data):
      
        
        etudiant = self.context.get('etudiant')
        cours_module = self.context.get('cours_module')

        if not etudiant or not cours_module:
            raise serializers.ValidationError("Étudiant ou module manquant dans le contexte.")

        # Injecter les données nécessaires
        validated_data['etudiant'] = etudiant
        validated_data['cours_module'] = cours_module
        validated_data['volume_horaire_total'] = extract_volume_as_int(cours_module.volume_horaire)
        validated_data['pourcentage_avancement'] = 0  # Initialisation à 0
        # Initialiser volume_horaire_restant pour le premier enregistrement
        #validated_data['volume_horaire_restant'] = validated_data['volume_horaire_total']
         # Calculer volume_horaire_restant
        validated_data['volume_horaire_restant'] = self.calculate_volume_horaire_restant(
            etudiant, cours_module, validated_data['volume_horaire_realise']
        )

         # Calculer le pourcentage d'avancement
        total_realise = AvancementCours.objects.filter(
            etudiant=etudiant,
            cours_module=cours_module
        ).aggregate(Sum('volume_horaire_realise'))['volume_horaire_realise__sum'] or 0

        # Ajouter le volume horaire réalisé actuellement en cours d'enregistrement
        total_realise += validated_data['volume_horaire_realise']

        # Calculer le pourcentage d'avancement
        pourcentage_avancement = (total_realise / validated_data['volume_horaire_total']) * 100

        # Enregistrer le pourcentage dans les données validées
        validated_data['pourcentage_avancement'] = pourcentage_avancement
        
        return super().create(validated_data)
"""
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image 
        fields = ['id','image', 'date_ajout']

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
import io
from django.core.files.uploadedfile import UploadedFile as DjangoUploadedFile

from rest_framework import serializers

from PIL import Image as PILImage
from django.core.exceptions import ValidationError
from io import BytesIO


class AvancementCoursSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.CharField(source='etudiant.nom_etudiant', read_only=True)
    image = serializers.ImageField(required=False)  # Champ image pour une seule image
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)
    class Meta:
        model = AvancementCours
        fields = [
            'id', 'etudiant_nom', 'cours_module', 'volume_horaire_total', 
            'volume_horaire_restant', 'volume_horaire_realise', 'pourcentage_avancement', 
            'heure_debut', 'heure_fin', 'date_op', 'image','image2','image3'
        ]
        read_only_fields = ['etudiant', 'cours_module', 'pourcentage_avancement', 
                            'date_op', 'volume_horaire_total', 'volume_horaire_restant']

    @staticmethod
    def calculate_volume_horaire_restant(etudiant, cours_module, volume_horaire_realise):
        """
        Calcule le volume horaire restant pour un étudiant et un module donnés.
        """
        # Vérifier si c'est le premier enregistrement pour cet étudiant et ce module
        if not AvancementCours.objects.filter(etudiant=etudiant, cours_module=cours_module).exists():
            # Si c'est le premier enregistrement, initialiser volume_horaire_restant avec volume_horaire_total
            return extract_volume_as_int(cours_module.volume_horaire) - volume_horaire_realise

        else:
            # Chercher l'avancement précédent de l'étudiant pour ce module là
            avancement_precedent = AvancementCours.objects.filter(
                etudiant=etudiant,
                cours_module=cours_module
            ).order_by('-date_op').first()  # Prendre le plus récent

            if avancement_precedent:
                # Calculer le volume horaire restant basé sur l'enregistrement précédent
                return avancement_precedent.volume_horaire_restant - volume_horaire_realise
            else:
                # Si aucun avancement précédent, calculer à partir du volume horaire total du module
                return extract_volume_as_int(cours_module.volume_horaire) - volume_horaire_realise

    def validate(self, data):
        image = data.get('image', None)
        
        if image:
            # Validation de l'image pour vérifier que c'est bien une image valide
            try:
                pil_image = PILImage.open(image)
                pil_image.verify()  # Vérifie que l'image est valide
                  # Après verify(), repositionner le pointeur pour que le fichier soit relu plus tard
                image.file.seek(0)
                #pil_image.close()
            except Exception:
                raise ValidationError({'image': 'L\'image doit être valide.'})

            # Vérification du type InMemoryUploadedFile
           
        
        return data

    def create(self, validated_data):
        request = self.context.get('request', None)
        image_data = request.FILES.get('image', None) if request else None
        image2_data = request.FILES.get('image2', None) if request else None
        image3_data = request.FILES.get('image3', None) if request else None

        etudiant = self.context.get('etudiant')
        cours_module = self.context.get('cours_module')

        if not etudiant or not cours_module:
            raise ValidationError("Étudiant ou module manquant dans le contexte.")

        # Enregistrer l'image si présente
        image_instance = None
        if image_data:
            try:
                # Vérifier que l'image est bien un InMemoryUploadedFile
                if isinstance(image_data, DjangoUploadedFile):
                    #image_instance = Image.objects.create(image=image_data)
                    pass
                else:
                    raise ValidationError("Le fichier d'image n'est pas valide.")
            except Exception as e:
                raise ValidationError(f"Erreur lors de l'enregistrement de l'image : {str(e)}")
        
         # Enregistrer l'image secondaire si présente
        image2_instance = None
        if image2_data:
            try:
                if isinstance(image2_data, DjangoUploadedFile):
                    #image2_instance = image2_data  #AvancementCours.objects.create(image=image2_data)
                    pass
                else:
                    raise ValidationError("Le fichier d'image 2 n'est pas valide.")
            except Exception as e:
                raise ValidationError(f"Erreur lors de l'enregistrement de l'image 2 : {str(e)}")

        image3_instance = None
        if image3_data:
            try:
                if isinstance(image3_data, DjangoUploadedFile):
                    #image3_instance = image3_data  #AvancementCours.objects.create(image=image2_data)
                    pass
                else:
                    raise ValidationError("Le fichier d'image 3 n'est pas valide.")
            except Exception as e:
                raise ValidationError(f"Erreur lors de l'enregistrement de l'image 3 : {str(e)}")



        # Créer l'objet `AvancementCours`
        validated_data['etudiant'] = etudiant
        validated_data['cours_module'] = cours_module
        validated_data['volume_horaire_total'] = extract_volume_as_int(cours_module.volume_horaire)
        validated_data['pourcentage_avancement'] = 0
        validated_data['volume_horaire_restant'] = self.calculate_volume_horaire_restant(
            etudiant, cours_module, validated_data.get('volume_horaire_realise')
        )
                
        # Injecter image principale et images secondaires si elles existent
        if image_instance:
            validated_data['image'] = image_instance.image  # ou juste image_instance selon ton modèle

        if image2_instance:
            validated_data['image2'] = image2_instance

        if image3_instance:
            validated_data['image3'] = image3_instance

         # Calculer le pourcentage d'avancement
        total_realise = AvancementCours.objects.filter(
            etudiant=etudiant,
            cours_module=cours_module
        ).aggregate(Sum('volume_horaire_realise'))['volume_horaire_realise__sum'] or 0
        
        # Ajouter le volume horaire réalisé actuellement en cours d'enregistrement
        total_realise += validated_data['volume_horaire_realise']

        # Calculer le pourcentage d'avancement
        pourcentage_avancement = (total_realise / validated_data['volume_horaire_total']) * 100

        # Enregistrer le pourcentage dans les données validées
        validated_data['pourcentage_avancement'] = pourcentage_avancement
        
        avancement_cours = AvancementCours.objects.create(**validated_data)

        # Associer l'image à `AvancementCours`
        if image_instance:
            avancement_cours.image = image_instance
        if image2_instance:
            avancement_cours.image = image2_instance
        if image3_instance:
            avancement_cours.image = image2_instance
        
        print("okk" ,validated_data['volume_horaire_restant'], total_realise, validated_data['volume_horaire_total'],validated_data['pourcentage_avancement'])

        avancement_cours.save()

        return avancement_cours
