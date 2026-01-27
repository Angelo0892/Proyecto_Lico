from django import template

register = template.Library()

@register.filter
def tiene_permiso(usuario, permiso):
    if not usuario or not hasattr(usuario, 'perfil'):
        return False
    return usuario.perfil.tiene_permiso(permiso)