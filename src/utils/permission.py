from rest_framework.permissions import BasePermission

class TienePermisoModelo(BasePermission):
    """
        Verificar si el usuario tiene permiso para realizar una accion
        sobre el modelo asociado a la vista
    """

    def has_permission(self, request, view):
        #Comprobar que la view tenga un atributo llamado model
        if not hasattr(view,'model'):
            return False
        
        model = view.model
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        #mapear metodos HTTP con los permisos
        metodo_permiso = {
            'GET' : f'{app_label}.view_{model_name}',
            'POST': f'{app_label}.add_{model_name}',
            'PUT': f'{app_label}.change_{model_name}',
            'PATH': f'{app_label}.change_{model_name}',
            'DELETE': f'{app_label}.delete_{model_name}',
        }
        
        #request.method obtiene el METODO HTTP de la PETICION
        permiso = metodo_permiso.get(request.method)

        #Si existe el permiso
        if permiso:
            #Concedo el permiso al usuario para la accion determinada
            return request.user.has_perm(permiso)
        
        return False




