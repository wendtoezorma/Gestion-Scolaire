# Generated by Django 5.0.7 on 2024-09-06 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0044_rename_nom_infos_titre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infos',
            name='contenu',
            field=models.FileField(blank=True, upload_to='infos/'),
        ),
    ]
