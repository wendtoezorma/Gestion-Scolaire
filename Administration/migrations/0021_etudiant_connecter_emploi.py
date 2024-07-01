# Generated by Django 5.0.6 on 2024-07-01 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0020_cours_module_professeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='Connecter',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.CreateModel(
            name='Emploi',
            fields=[
                ('Id_emploi', models.AutoField(primary_key=True, serialize=False)),
                ('jour', models.CharField(choices=[('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')], max_length=10)),
                ('heure_debut', models.TimeField()),
                ('heure_fin', models.TimeField()),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administration.professeurs')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Administration.cours_module')),
            ],
            options={
                'verbose_name': 'Emploi',
                'verbose_name_plural': 'Emplois',
                'ordering': ['jour', 'heure_debut'],
            },
        ),
    ]
