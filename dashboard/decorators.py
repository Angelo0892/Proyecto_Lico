from django.shortcuts import redirect
from django.contrib import messages

def permiso_requerido(nombre_permiso):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            perfil = getattr(request.user, 'perfil', None)

            if not perfil or not perfil.tiene_permiso(nombre_permiso):
                messages.error(request, "No tienes permisos para realizar esta acción.")
                return redirect('dashboard:principal')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
