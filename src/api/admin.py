from django.contrib import admin
from .models import Estudiante, Curso, Modulo, Inscripcion

# Register your models here.
admin.site.register(Estudiante)
admin.site.register(Curso)
admin.site.register(Modulo)
admin.site.register(Inscripcion)