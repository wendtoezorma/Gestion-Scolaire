# Generated by Django 4.0 on 2024-07-29 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0026_rename_etudiant_prix_scolarite_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prix_scolarite',
            old_name='student',
            new_name='etudiant',
        ),
    ]
