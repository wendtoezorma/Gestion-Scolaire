# Generated by Django 5.0.6 on 2024-07-18 02:03

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filiere',
            fields=[
                ('Id_filiere', models.AutoField(primary_key=True, serialize=False)),
                ('nom_filiere', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ['nom_filiere'],
            },
        ),
        migrations.CreateModel(
            name='professeurs',
            fields=[
                ('Id_prof', models.AutoField(primary_key=True, serialize=False)),
                ('nom_prof', models.CharField(max_length=150)),
                ('prenom_prof', models.CharField(max_length=300)),
                ('email_prof', models.EmailField(max_length=400)),
                ('niveau_prof', models.CharField(choices=[('Selectionner', 'Selectionner'), ('Docteur', 'Docteur'), ('Professeur', 'Professeur'), ('C', 'Ingénieur'), ('Lamda', 'Lamda'), ('Vacataire', 'Vacataire')], default='Selectionner', max_length=20)),
                ('mdp_prof', models.CharField(blank=True, max_length=600)),
                ('numero_prof', models.CharField(max_length=20)),
                ('date_ajout', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'professeur',
                'verbose_name_plural': 'professeurs',
                'ordering': ['-date_ajout'],
            },
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('matricule', models.BigAutoField(primary_key=True, serialize=False)),
                ('nom_etudiant', models.CharField(max_length=200)),
                ('prenom_etudiant', models.CharField(max_length=270)),
                ('email_etudiant', models.EmailField(max_length=254, unique=True)),
                ('telephone_etudiant', models.CharField(max_length=200)),
                ('sexe_etudiant', models.CharField(choices=[('Selectionner', 'Selectionner'), ('Masculin', 'Masculin'), ('Feminin', 'Feminin')], default='Selectionner', max_length=13)),
                ('Date_naiss_etudiant', models.DateField()),
                ('lieu_naiss_etudiant', models.CharField(max_length=200)),
                ('nationalite_etudiant', models.CharField(max_length=200)),
                ('niveau_etudiant', models.CharField(choices=[('LICENCE1', 'LICENCE1'), ('LICENCE2', 'LICENCE2'), ('LICENCE3', 'LICENCE3'), ('MASTER1', 'MASTER1'), ('MASTER2', 'MASTER2'), ('DOCTORAT', 'DOCTORAT')], default='Selectionner', max_length=200)),
                ('annee_academique_etudiant', models.CharField(max_length=100)),
                ('mdp_etudiant', models.CharField(blank=True, max_length=200)),
                ('date_ajout', models.DateField(auto_now=True)),
                ('password_updated', models.BooleanField(default=False)),
                ('boursier', models.BooleanField(default=False, null=True)),
                ('Connecter', models.BooleanField(default=False, null=True)),
                ('filiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='etudiants', to='Administration.filiere')),
            ],
            options={
                'verbose_name': 'Etudiant',
                'verbose_name_plural': 'Etudiants',
                'ordering': ['nom_etudiant'],
            },
        ),
        migrations.CreateModel(
            name='Cours_Module',
            fields=[
                ('Id_module', models.AutoField(primary_key=True, serialize=False)),
                ('nom_module', models.CharField(max_length=250)),
                ('credit_module', models.IntegerField()),
                ('volume_horaire', models.CharField(max_length=10)),
                ('date_ajout', models.DateField(auto_now=True)),
                ('filiere', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cours', to='Administration.filiere')),
                ('professeur', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='Administration.professeurs')),
            ],
            options={
                'verbose_name': 'Cours_Module',
                'verbose_name_plural': 'Cours_Modules',
                'ordering': ['nom_module'],
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('Id_note', models.AutoField(primary_key=True, serialize=False)),
                ('Note1', models.FloatField(default=0)),
                ('Note2', models.FloatField(default=0)),
                ('moyenne', models.FloatField(default=0.0, editable=False)),
                ('etudiant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='Administration.etudiant')),
                ('matiere_module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='Administration.cours_module')),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
                'ordering': ['matiere_module'],
            },
        ),
        migrations.CreateModel(
            name='Enseignement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ajout', models.DateField(auto_now=True)),
                ('module_enseigner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursenseigner', to='Administration.cours_module')),
                ('professeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prof', to='Administration.professeurs')),
            ],
            options={
                'verbose_name': 'Enseignement',
                'verbose_name_plural': 'Enseignements',
                'ordering': ['date_ajout'],
            },
        ),
        migrations.CreateModel(
            name='Emploi',
            fields=[
                ('Id_emploi', models.AutoField(primary_key=True, serialize=False)),
                ('jour', models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')], max_length=10)),
                ('heure_debut', models.TimeField()),
                ('heure_fin', models.TimeField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administration.cours_module')),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administration.professeurs')),
            ],
            options={
                'verbose_name': 'Emploi',
                'verbose_name_plural': 'Emplois',
                'ordering': ['jour', 'heure_debut'],
            },
        ),
        migrations.CreateModel(
            name='Scolarite',
            fields=[
                ('Id_scolarite', models.AutoField(primary_key=True, serialize=False)),
                ('tranche_1', models.FloatField(default=0)),
                ('tranche_2', models.FloatField(default=0)),
                ('tranche_3', models.FloatField(default=0)),
                ('total', models.FloatField(default=0, editable=False)),
                ('Montant_restant', models.FloatField(default=0.0, editable=False)),
                ('date_payement', models.DateField(auto_now=True)),
                ('etudiant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scolarite', to='Administration.etudiant')),
            ],
            options={
                'verbose_name': 'Scolarite',
                'verbose_name_plural': 'Scolarite',
                'ordering': ['-date_payement'],
            },
        ),
        migrations.CreateModel(
            name='Administration',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=False, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('Identifiant', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=150)),
                ('prenom', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=300, unique=True)),
                ('Numero', models.CharField(max_length=15)),
                ('date_naissance', models.DateField()),
                ('num_CNIB', models.CharField(max_length=20)),
                ('sexe', models.CharField(choices=[('SELECTIONNER', 'SELECTIONNER'), ('MASCULIN', 'MASCULIN'), ('FEMININ', 'FEMININ')], default='SELECTIONNER', max_length=12)),
                ('date_ajout', models.DateField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='administration_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='administration_user_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Administration',
                'verbose_name_plural': 'Administrations',
                'ordering': ['-date_ajout'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
