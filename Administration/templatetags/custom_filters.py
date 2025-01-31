# myapp/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def mul(value1, value2):
    return value1 * value2
"""
# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
"""
# templatetags/extras.py

from django import template

register = template.Library()

@register.filter
def get_item(value, arg):
    """Récupère un élément d'une liste par son index."""
    try:
        return value[int(arg)]
    except (IndexError, ValueError):
        return ''
"""
@register.filter
def get_note_at_index(notes_dict, matricule, index):
    try:
        notes = notes_dict[matricule]
        return notes[index] if index < len(notes) else ''
    except KeyError:
        return ''
"""
@register.filter
def concat_values(value1, value2):
    """
    Concatène deux valeurs avec un séparateur '_'.
    """
    return f"{value1}_{value2}"

@register.filter
def get_note_at_index(notes, args):
    """
    Récupère la note à un index spécifique dans la liste des notes.
    'notes' est une liste de notes et 'args' contient l'index et le matricule de l'étudiant sous forme de 'index_matricule'.
    """
    try:
        # Décomposer les arguments passés en index et matricule
        index, matricule = args.split('_')
        index = int(index)
        # Ici, nous faisons attention au matricule, mais dans votre exemple, il n'est pas utilisé directement.
        return notes[index]  # Si matricule est nécessaire pour une autre logique, vous pouvez l'ajouter.
    except (ValueError, IndexError):
        return None
