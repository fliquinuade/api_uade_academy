from django.contrib import admin
from .models import Estudiante, Curso, Modulo, Inscripcion, CustomUser

# Register your models here.
admin.site.register(Estudiante)
admin.site.register(Modulo)
admin.site.register(Inscripcion)
admin.site.register(CustomUser)

class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1

class InscripcionInline(admin.TabularInline):
    model = Inscripcion
    
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id','course_number','name','level','cost')
    #Especifico campos de busqueda para el input search
    search_fields = ('name','description')
    list_filter = ('level','start_date')
    ordering = ('course_number','start_date')
    #limite de paginacion
    list_per_page=10
    inlines = [ModuloInline, InscripcionInline]
    #readonly_fields = ('image',)