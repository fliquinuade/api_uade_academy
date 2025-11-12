# Guia para el Agente AI - API UADE Academy

Este documento contiene instrucciones necesarias para el agente IA con las reglas, estandares y practicas para el desarrollo de la API UADE Academy.

## Stack y Versiones
- **Python**: 3.13
- **Django**: 5.2.3
- **Django REST Framework**: 3.16
Para demas dependencias consultar el archivo requirements.txt para ver las dependencias y versiones utilizadas en el proyecto.

## Arquitectura del Proyecto
El proyecto sigue una arquitectura modular basada en Django y Django REST Framework. La estructura de directorios es la siguiente:
```
api_uade_academy/
├── src/
│   ├── api/
│   │   ├── models.py # Modelos de datos
│   │   ├── serializers.py # Serializadores para convertir modelos a JSON
│   │   ├── views.py # Vistas y endpoints de la API
│   │   ├── urls.py # Rutas de la API
│   ├── config/
│   │   ├── settings.py # Configuración del proyecto
│   │   ├── urls.py # Rutas principales del proyecto
│   ├── manage.py # Script de gestión de Django
└── requirements.txt # Dependencias del proyecto
```

### Reglas y Estándares
1. Models.py se definen unicamente los modelos de datos.
2. Serializers.py se encargan de la serialización y deserialización de los modelos. Se deben incluir serializados de lectura y escritura, segun corresponda.
3. Views.py contiene las vistas y endpoints de la API. Se deben utilizar APIView o ViewSets segun corresponda.

## Estilos
- Seguir las convenciones de PEP 8 para Python.
- Utilizar nombres descriptivos en español para variables, funciones y clases.
- Documentar con docstrings todas las funciones y clases.

## Entregables
- El codigo necesario segun sea solicitado por el usuarios.
- No incluir explicaciones o comentarios adicionales a menos que se solicite.
- No generer archivos README a menos que se solicite especificamente.




