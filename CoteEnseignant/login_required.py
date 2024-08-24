from functools import wraps
from django.shortcuts import redirect


def professeur_login_required(view_func):
    from .views import connexion_Prof
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'professeur_id' not in request.session:
            return redirect('connexion_Prof')  # Redirige vers la page de connexion des professeurs
        return view_func(request, *args, **kwargs)
    return _wrapped_view
