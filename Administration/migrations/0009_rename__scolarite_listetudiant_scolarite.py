# Generated by Django 4.0 on 2024-07-26 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0008_remove_etudiant_montant_total_verse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listetudiant',
            old_name='_scolarite',
            new_name='scolarite',
        ),
    ]
