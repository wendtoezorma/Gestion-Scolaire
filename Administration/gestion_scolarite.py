from .models import *




# gestion_scolarite.py

def calculate_total(self):
    montant = 0.0

    # Définir les frais de scolarité de base en fonction du niveau et de la filière
    if self.etudiant.niveau_etudiant == 'LICENCE1':
        if self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)', "BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            montant = 600000.00
        elif self.etudiant.filiere.nom_filiere == 'GENIE LOGICIEL (GL)':
            montant = 700000.00
        elif self.etudiant.filiere.nom_filiere in ['COMPTABILITE', 'ECONOMIE ET STATISTIQUE (ESA)']:
            montant = 450000.00
    
    elif self.etudiant.niveau_etudiant == 'LICENCE2':
        if self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)', "BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            montant = 750000.00
        elif self.etudiant.filiere.nom_filiere == 'GENIE LOGICIEL (GL)':
            montant = 850000.00
        elif self.etudiant.filiere.nom_filiere in ['COMPTABILITE', 'ECONOMIE ET STATISTIQUE (ESA)']:
            montant = 600000.00
    
    elif self.etudiant.niveau_etudiant == 'LICENCE3':
        if self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)', "BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            montant = 850000.00
        elif self.etudiant.filiere.nom_filiere == 'GENIE LOGICIEL (GL)':
            montant = 1050000.00
        elif self.etudiant.filiere.nom_filiere in ['COMPTABILITE', 'ECONOMIE ET STATISTIQUE (ESA)']:
            montant = 750000.00
    
    elif self.etudiant.niveau_etudiant == 'MASTER1':
        if self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)', "BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            montant = 1050000.00
        elif self.etudiant.filiere.nom_filiere == 'GENIE LOGICIEL (GL)':
            montant = 1450000.00
        elif self.etudiant.filiere.nom_filiere in ['COMPTABILITE', 'ECONOMIE ET STATISTIQUE (ESA)']:
            montant = 950000.00
    
    elif self.etudiant.niveau_etudiant == 'MASTER2':
        if self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)', "BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            montant = 1350000.00
        elif self.etudiant.filiere.nom_filiere == 'GENIE LOGICIEL (GL)':
            montant = 2350000.00
        elif self.etudiant.filiere.nom_filiere in ['COMPTABILITE', 'ECONOMIE ET STATISTIQUE (ESA)']:
            montant = 1250000.00
    
    # Appliquer les réductions pour les étudiants boursiers
    if self.etudiant.bourse:
        if self.etudiant.bourse.type_bourse == 'boursier_etat':
            # Seulement frais d'inscription par exemple
            montant = 45000.00  # Exemple de frais d'inscription
        else:
            montant *= (self.etudiant.bourse.reduction)

    return montant 

def totaux(self):
    pass