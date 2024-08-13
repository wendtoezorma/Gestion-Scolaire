# Generated by Django 4.0 on 2024-07-28 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0016_coursfichier_annee_academique_cour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursfichier',
            name='niveau_etudiant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fichierNiveau', to='Administration.etudiant'),
        ),
        migrations.AlterField(
            model_name='coursfichier',
            name='filiere',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fichier', to='Administration.filiere'),
        ),
    ]
