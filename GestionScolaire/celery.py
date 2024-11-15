from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Spécifie le module de configuration par défaut de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionScolaire.settings')

# Créez l'application Celery
app = Celery('GestionScolaire')

# Charge la configuration de Celery depuis Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover les tâches dans toutes les applications Django installées
app.autodiscover_tasks()

# Exemple de tâche Celery
@app.task
def verifier_etudiants_task():
    # Importation explicite du module qui contient la fonction
    from api.views import verifier_etudiants_connectes
    verifier_etudiants_connectes(None)

# Planification de la tâche avec Celery Beat
app.conf.beat_schedule = {
    'verifier-etudiants-toutes-les-1-minutes': {
        'task': 'GestionScolaire.celery.py.celery.verifier_etudiants_task',  # Chemin complet de la tâche
        'schedule': crontab(minute='*/1'),  # Exécuter toutes les minutes
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
