
def apercu_caisse():
    from django.shortcuts import render
    from django.db.models import Sum
    from .models import Scolarite
    tranches = Scolarite.objects.aggregate(
        total_tranche_1=Sum('tranche_1'),
        total_tranche_2=Sum('tranche_2'),
        total_tranche_3=Sum('tranche_3')
    )
    total_general = (tranches['total_tranche_1'] or 0) + (tranches['total_tranche_2'] or 0) + (tranches['total_tranche_3'] or 0)
    return total_general or 0.0
