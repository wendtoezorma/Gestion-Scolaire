
from django.shortcuts import render
from django.db.models import Sum
from .models import Scolarite
"""def apercu_caisse():
    
    tranches = Scolarite.objects.aggregate(
        total_tranche_1=Sum('tranche_1'),
        total_tranche_2=Sum('tranche_2'),
        total_tranche_3=Sum('tranche_3')
    )
    total_general = (tranches['total_tranche_1'] or 0) + (tranches['total_tranche_2'] or 0) + (tranches['total_tranche_3'] or 0)
    return total_general or 0.0
"""
from django.db.models import Sum
from django.db.models import F
from .models import Scolarite
import json

def apercu_caisse():
    # On commence par récupérer les objets 'Scolarite' et traiter les tranches.
    total_general = 0

    # Récupérer toutes les entrées de scolarité
    scolarites = Scolarite.objects.all()
    
    for scolarite in scolarites:
        # On suppose que 'tranches' est une liste dans le champ JSON
        tranches = scolarite.tranches  # Assurez-vous que c'est une liste de floats

        # Additionner les tranches si elles existent
        if tranches:
            total_general += sum(tranches)  # Somme des valeurs de la liste
        
    return total_general




from .models import Etudiant
def nombre_etudiants_connecter():
    
    etudiant_connecter = Etudiant.objects.filter(Connecter=True).count()
    
    return  etudiant_connecter or 0
  