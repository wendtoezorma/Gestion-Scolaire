from typing import Iterable
from django.db import models
from  django.contrib.auth.models import AbstractUser
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin, Group, Permission
from django.contrib.auth.hashers import make_password, check_password


#La classe Filiere
class Filiere(models.Model):
    Id_filiere = models.AutoField(primary_key=True)
    nom_filiere = models.CharField(max_length=250)

    class Meta:
        ordering = ['nom_filiere']

    def __str__(self):
        return self.nom_filiere
    

########## La table des professeurs ###########
class professeurs(models.Model):
    Id_prof = models.AutoField(primary_key=True)
    nom_prof = models.CharField(max_length=150)
    prenom_prof = models.CharField(max_length=300)
    email_prof = models.EmailField(max_length=400)
    ##### Creons à présent une liste pour la sélection du niveau des professeurs
    niv_prof = [
        ("Selectionner","Selectionner"),
        ("Docteur","Docteur"),
        ("Professeur","Professeur"),
        ("Ing","Ingénieur"),
        ("Lamda","Lamda"),
        ("Vacataire","Vacataire"),
    ]
    niveau_prof = models.CharField(max_length=20,choices=niv_prof,default="Selectionner")
    mdp_prof = models.CharField(max_length=600,blank=True)
    numero_prof = models.CharField(max_length=20)
    #filiere = models.ForeignKey(Filiere,related_name='filiereprof',on_delete=models.CASCADE,null=True)
    #module_enseigner = models.ForeignKey(Cours_Module,related_name='coursenseigner',on_delete=models.CASCADE,null=True)
    date_ajout = models.DateField(auto_now=True)
    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "professeur"
        verbose_name_plural = "professeurs"
    

    def __str__(self):
        if (self.niveau_prof=="Lamda" or self.niveau_prof=="Vacataire"):
            self.niveau_prof="Mr"
            
        elif (self.niveau_prof=="Docteur"):
            self.niveau_prof="Dr"
            
        elif (self.niveau_prof=="Professeur"):
            self.niveau_prof="Pr"
            
        elif (self.niveau_prof=="Professeur"):
            self.niveau_prof="Ing"
            
        return f"{self.niveau_prof}.{self.nom_prof} {self.prenom_prof}"
    
    
    def save(self, *args, **kwargs):
        # Hacher le mot de passe avant d'enregistrer l'objet, mais ne pas mettre à jour password_updated ici
        if self.pk is None and self.mdp_prof:
            self.mdp_prof = make_password(self.mdp_prof)
        super().save(*args, **kwargs)
    
    
    

    def set_password(self, password):
        self.mdp_prof = make_password(password)

    def check_password(self, password):
        return check_password(password, self.mdp_prof)
    
    

class Boursier(models.Model):
    TYPE_CHOICES = [
        ('non_boursier', 'Non Boursier'),
        ('boursier_etat', "Boursier de l'Etat"),
        ('boursier_particulier_50', 'Boursier Particulier 50%'),
        ('boursier_particulier_75', 'Boursier Particulier 75%'),
    ]
    type_bourse = models.CharField(max_length=50, choices=TYPE_CHOICES, default='non_boursier')
    reduction = models.FloatField(default=0.0) 

    def __str__(self):
        return self.type_bourse
from django.core.validators import MinLengthValidator
import re
from .gestion_scolarite import calculate_total 
from django.core.exceptions import ValidationError
def validate_password_special_char(value):
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(
            "Le mot de passe doit contenir au moins un caractère spécial : !@#$%^&*(),.?\":{}|<>"
        )
class Etudiant(models.Model):
    matricule = models.BigAutoField(primary_key=True)
    nom_etudiant = models.CharField(max_length=200)
    prenom_etudiant = models.CharField(max_length=270)
    email_etudiant = models.EmailField(unique=True)
    telephone_etudiant = models.CharField(max_length=200)
    
    choix_sexe = [
        ('Selectionner', "Selectionner"),
        ('Masculin', "Masculin"),
        ('Feminin', "Feminin")
    ]
    sexe_etudiant = models.CharField(max_length=13, choices=choix_sexe, default='Selectionner')
    Date_naiss_etudiant = models.DateField()
    lieu_naiss_etudiant = models.CharField(max_length=200)
    nationalite_etudiant = models.CharField(max_length=200)
    niveau_etudiant = models.CharField(max_length=200, choices=[
        ('LICENCE1', "LICENCE1"),
        ('LICENCE2', "LICENCE2"),
        ('LICENCE3', "LICENCE3"),
        ('MASTER1', "MASTER1"),
        ('MASTER2', "MASTER2"),
        ('DOCTORAT', "DOCTORAT"),
    ], default='Selectionner')
    annee_academique_etudiant = models.CharField(max_length=100, choices=[
        ('2022/2023', "2022/2023"),
        ('2023/2024', "2023/2024"),
        ('2024/2025', "2024/2025"),
        ('2025/2026', "2025/2026"),
        ('2026/2027', "2026/2027"),
        ('2027/2028', "2027/2028"),
        ('2028/2029', "2028/2029"),
    ], default='Selectionner')
    mdp_etudiant = models.CharField(max_length= 9, blank=True,validators=[validate_password_special_char, MinLengthValidator(8)])
    date_ajout = models.DateField(auto_now=True)
    filiere = models.ForeignKey(Filiere, related_name='etudiants', on_delete=models.CASCADE, null=True)
    password_updated = models.BooleanField(default=False)
    bourse = models.ForeignKey(Boursier, on_delete=models.SET_NULL, null=True, blank=True)
    Connecter = models.BooleanField(default=False, null=True)
    
    # Nouveau champ pour la photo de l'étudiant
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    
     
    class Meta:
        ordering = ['nom_etudiant']
        verbose_name = "Etudiant"
        verbose_name_plural = "Etudiants"
      
    
    def __str__(self):
        return f"{self.nom_etudiant} {self.prenom_etudiant} || {self.filiere} || {self.niveau_etudiant}"
    
    #def save(self, *args, **kwargs):
        # Hacher le mot de passe avant d'enregistrer l'objet
        #if self.mdp_etudiant and not self.password_updated:
            #self.mdp_etudiant = make_password(self.mdp_etudiant)
            #self.password_updated = True
        #super().save(*args, **kwargs)

    
    
    def set_password(self, raw_password):
        self.mdp_etudiant = make_password(raw_password)
        self.password_updated = True
        self.save()
    
        
    def set_password1(self, raw_password):
        self.mdp_etudiant = make_password(raw_password)
        self.save()


    def check_password(self, raw_password):
        return check_password(raw_password, self.mdp_etudiant)
    
    def get_filiere_display(self):
        if self.filiere:
            return self.filiere.nom_filiere
        return "Non spécifié"
 
    
class Cours_Module(models.Model):
    Id_module = models.AutoField(primary_key=True)
    nom_module = models.CharField(max_length=250)
    credit_module = models.IntegerField()#limiter le nombre de chifre a 2 chiffre
    volume_horaire = models.CharField(max_length=10)
    date_ajout = models.DateField(auto_now=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='cours',default=1)
    professeur = models.ForeignKey(professeurs, on_delete=models.CASCADE, related_name='modules',default=1)
    niveau = models.CharField(max_length=200, choices=[
        ('LICENCE1', "LICENCE1"),
        ('LICENCE2', "LICENCE2"),
        ('LICENCE3', "LICENCE3"),
        ('MASTER1', "MASTER1"),
        ('MASTER2', "MASTER2"),
        ('DOCTORAT', "DOCTORAT"),
    ], default='Selectionner')

    class Meta:
        ordering = ['nom_module']
        verbose_name = "Cours_Module"
        verbose_name_plural = "Cours_Modules"


    def __str__(self):
        return self.nom_module
    

class Notes(models.Model):
    Id_note = models.AutoField(primary_key=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes', null=True)
    matiere_module = models.ForeignKey(Cours_Module, on_delete=models.CASCADE, related_name='modules', null=True)
    Note1 = models.FloatField(default=0)
    Note2 = models.FloatField(default=0)
    moyenne = models.FloatField(editable=False, default=0.0)
    #Concerne= Etudiant.nom_etudiant
    class Meta:
        ordering = ['matiere_module']
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        
    def save(self, *args, **kwargs):
        self.moyenne = (self.Note1 + self.Note2) / 2
        super(Notes, self).save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.etudiant.nom_etudiant} - {self.matiere_module.nom_module} - Moyenne: {self.moyenne}"
# La classe étudiant à présent
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


    # Pas de méthode create_superuser ici
    # Les superutilisateurs seront gérés par le modèle User par défaut de Django
from .managers import AdministrationManager
# La classe étudiant à présent
class Administration(AbstractBaseUser, PermissionsMixin):
    Identifiant = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=250)
    email = models.EmailField(max_length=300, unique=True)
    Numero = models.CharField(max_length=15)
    date_naissance = models.DateField()
    num_CNIB = models.CharField(max_length=20)
    choix_sexe = [
        ('SELECTIONNER', "SELECTIONNER"),
        ('MASCULIN', "MASCULIN"),
        ('FEMININ', "FEMININ")
    ]
    sexe = models.CharField(max_length=12, choices=choix_sexe, default='SELECTIONNER')
    date_ajout = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)#actif automatiquement 
    is_staff = models.BooleanField(default=False)# par defaut il n'est pas admin 
    #mot_de_passe = models.CharField(max_length=500, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='administration_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='administration_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'email'  # Le champ utilisé pour l'identification des utilisateurs
    REQUIRED_FIELDS = ['nom', 'prenom', 'Numero', 'date_naissance', 'num_CNIB', 'sexe']  # Champs requis pour créer un utilisateur
    objects = AdministrationManager()
    class Meta:
        ordering = ['-date_ajout']
        #db_table = 'Administration' Pour renommer la table
        verbose_name = "Administration"
        verbose_name_plural = "Administrations"

    def __str__(self):
        return self.nom
    
    

    @staticmethod
    def create_superuser(email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = Administration(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=user._db)
        return user





############# On crée à ce niveau une classe pour prof et filiere ######### 
class Enseignement(models.Model):
    professeur=models.ForeignKey(professeurs,related_name='prof',on_delete=models.CASCADE)
    module_enseigner = models.ForeignKey(Cours_Module,related_name='coursenseigner',on_delete=models.CASCADE)
    date_ajout = models.DateField(auto_now=True)
    #affiche_prenom_prof=professeur.prenom_prof
    #affiche_nom_prof =professeur.nom_prof
    #affiche_module_prof =module_enseigner.nom_module
    class Meta:
        ordering = ['date_ajout']
        verbose_name = "Enseignement"
        verbose_name_plural = "Enseignements"
    
    def __str__(self):
        return self.professeur.nom_prof
    
######### La table pour la gestion de scolarité #########
class Scolarite(models.Model):
    Id_scolarite = models.AutoField(primary_key=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='scolarite', null=True)
    tranche_1 = models.FloatField(default=0)
    tranche_2 = models.FloatField(default=0)
    tranche_3 = models.FloatField(default=0)
    total = models.FloatField(default=0, editable=False)
    Montant_restant = models.FloatField(editable=False, default=0.0)
    montant_total_verse = models.FloatField(editable=False, default=0.0)
    
    date_payement = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-date_payement']
        verbose_name = "Scolarite"
        verbose_name_plural = "Scolarite"
    
    #####Importons la bibliothèque qui gère la scolarité en fonction de la filiere et du niveau d'étude
        
    from .gestion_scolarite import calculate_total    
    def save(self, *args, **kwargs):
        self.total = self.calculate_total()
        self.montant_total_verse=(self.tranche_1 + self.tranche_2 + self.tranche_3)
        self.Montant_restant = self.total - self.montant_total_verse
        super(Scolarite, self).save(*args, **kwargs)


    def __str__(self):
        return f"Payement de {self.etudiant.nom_etudiant} {self.etudiant.prenom_etudiant} {self.etudiant.filiere} {self.etudiant.niveau_etudiant}"
    
    @classmethod
    def get_totaux(cls):
        return cls.objects.aggregate(total_sum=models.Sum('total'))['total_sum'] or 0
    


class Emploi(models.Model):
    Id_emploi = models.AutoField(primary_key=True)
    module = models.ForeignKey(Cours_Module, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(professeurs, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10, choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')])
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        ordering = ['jour', 'heure_debut']
        verbose_name = "Emploi"
        verbose_name_plural = "Emplois"

    def __str__(self):
        return f"{self.module.nom_module} ({self.enseignant.nom_prof}) - {self.jour} {self.heure_debut} - {self.heure_fin}"

from django.db import models

class UploadedFile(models.Model):
    file = models. FileField(upload_to='uploaded_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.name
        
############################## Les TD COURS ET ANCIENS SUJETS #################

class CoursFichier(models.Model):
    Id_fichier = models.AutoField(primary_key=True)
    nom_fichier = models.CharField(max_length=250)
    fichier = models.FileField(upload_to='cours/')
    date_ajout = models.DateField(auto_now=True)
    professeur = models.ForeignKey(professeurs, on_delete=models.CASCADE, related_name='cours_fichiers')
    module = models.ForeignKey(Cours_Module, on_delete=models.CASCADE, related_name='fichiers')
    filiere = models.ForeignKey(Filiere,on_delete=models.CASCADE, related_name='fichier',null=True)
    niveau = models.CharField(max_length=200, choices=[
        ('LICENCE1', "LICENCE1"),
        ('LICENCE2', "LICENCE2"),
        ('LICENCE3', "LICENCE3"),
        ('MASTER1', "MASTER1"),
        ('MASTER2', "MASTER2"),
        ('DOCTORAT', "DOCTORAT"),
    ], default='Selectionner')
    annee_academique_cour = models.CharField(max_length=100, choices=[
        ('2022/2023', "2022/2023"),
        ('2023/2024', "2023/2024"),
        ('2024/2025', "2024/2025"),
        ('2025/2026', "2025/2026"),
        ('2026/2027', "2026/2027"),
        ('2027/2028', "2027/2028"),
        ('2028/2029', "2028/2029"),
    ], default='Selectionner')
    type_fichier = models.CharField(max_length=200, choices=[
        ('Cours', "Cours"),
        ('TD', "TD"),
        ('Devoir 1', "Devoir 1"),
        ('Devoir 2', "Devoir 2"),
        ('Devoir Session ', "Devoir Session"),
    ], default='Selectionner')
    
    class Meta: 
        ordering = ['date_ajout']
        verbose_name = "Cours Fichier"
        verbose_name_plural = "Cours Fichiers"

    def __str__(self):
        return self.nom_fichier

#################### POUR LES INFORMATIONS A AFFICHER DANS L'APP MOBILE ####

class Infos(models.Model):
    id_infos = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=200)
    message=models.TextField(max_length=100000)
    contenu=models.FileField(upload_to="infos/",blank=True)
    date_creation=models.DateField(auto_now=True)
    class Meta: 
        ordering = ['date_creation']
        verbose_name = "info"
        verbose_name_plural = "infos"

    def __str__(self):
        return self.titre
