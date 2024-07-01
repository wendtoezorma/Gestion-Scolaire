from .models import *




def calculate_total(self):
    #user = str(Etudiant.boursier)
        #####################################   SCOLARITE TECHNOLOGIE     #######################################################################
    #if user=="0":
        if self.etudiant.niveau_etudiant == 'LICENCE1' and self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)',"BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            return 600000.00
        
        elif self.etudiant.niveau_etudiant == 'LICENCE2' and self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)',"BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            return 750000.00
        
        elif self.etudiant.niveau_etudiant == 'LICENCE3' and self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)',"BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            return 850000.00
        
        elif self.etudiant.niveau_etudiant == 'MASTER1' and self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)',"BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            return 1050000.00
        
        elif self.etudiant.niveau_etudiant == 'MASTER2' and self.etudiant.filiere.nom_filiere in ['ELECTRONIQUE ET INFORMATIQUE INDUSTRIEL (EII)',"BATIMENT ET TRAVAUX PUBLIC (BTP)", 'RESEAUX ET TELECOMMUNICATIONS (RT)', 'ELECTROTECH (ET)']:
            return 1350000.00
        
        
        #####################################   SCOLARITE GENIE LOGICIEL      #######################################################################
        
        
        elif self.etudiant.niveau_etudiant == 'LICENCE1' and self.etudiant.filiere.nom_filiere in ['GENIE LOGICIEL (GL)']:
            return 700000.00
        
        elif self.etudiant.niveau_etudiant == 'LICENCE2' and self.etudiant.filiere.nom_filiere in ['GENIE LOGICIEL (GL)']:
            return 850000.00
        
        elif self.etudiant.niveau_etudiant == 'LICENCE3' and self.etudiant.filiere.nom_filiere in ['GENIE LOGICIEL (GL)']:
            return 1050000.00
        
        elif self.etudiant.niveau_etudiant == 'MASTER1' and self.etudiant.filiere.nom_filiere in ['GENIE LOGICIEL (GL)']:
            return 1450000.00
        
        elif self.etudiant.niveau_etudiant == 'MASTER2' and self.etudiant.filiere.nom_filiere in ['GENIE LOGICIEL (GL)']:
            return 2350000.00
        
        #####################################   SCOLARITE Management     #######################################################################
        
        
        if self.etudiant.niveau_etudiant == 'LICENCE1' and self.etudiant.filiere.nom_filiere in ['COMPTABILITE','ECONOMIE ET STATISTIQUE (ESA)']:
            return 450000.00
        
        elif self.etudiant.niveau_etudiant == 'LICENCE2' and self.etudiant.filiere.nom_filiere in ['COMPTABILITE','ECONOMIE ET STATISTIQUE (ESA)']:
            return 600000.00
        
        elif self.etudiant.niveau_etudiant == 'LICENCE3' and self.etudiant.filiere.nom_filiere in ['COMPTABILITE','ECONOMIE ET STATISTIQUE (ESA)']:
            return 750000.00
        
        elif self.etudiant.niveau_etudiant == 'MASTER1' and self.etudiant.filiere.nom_filiere in ['COMPTABILITE','ECONOMIE ET STATISTIQUE (ESA)']:
            return 950000.00
        
        elif self.etudiant.niveau_etudiant == 'MASTER2' and self.etudiant.filiere.nom_filiere in ['COMPTABILITE','ECONOMIE ET STATISTIQUE (ESA)']:
            return 1250000.00
        
        
    
    # Ajoutez ici d'autres conditions pour d'autres combinaisons de filières et niveaux
        return 0.0