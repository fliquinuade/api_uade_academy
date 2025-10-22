from rest_framework import serializers
from .models import Curso, Estudiante, Modulo, Inscripcion
from datetime import date
import re

def validar_caracteres_alfebeticos(value):
    """
        Una funcion generica que verifica si el valor posee caracteres alfabeticos
    """
    if not re.match(r'[a-zA-Z\s]+$',value):
        raise serializers.ValidationError('El valor debe ser alfabetico')


class ModuloSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        max_length=100,
        validators = [validar_caracteres_alfebeticos]
    )

    class Meta:
        model = Modulo
        fields = ['nombre','duracion','curso','ficha']
        depth = 1

class ModuloWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modulo
        fields = '__all__'

    def validate_ficha(self, file):
        #Validar el tamaño del archivo 2MB
        if file.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("El archivo debe tener 2MB como máximo")
        #Validar el tipo de archivo - content_type
        if file.content_type not in {"image/jpeg","image/png"}:
            raise serializers.ValidationError("Solo JPG/PNG")        
        return file

    
class CursoSerializer(serializers.ModelSerializer):
    """
        Serializado de curso para operaciones de crear/actualizar
    """
    name = serializers.CharField(
        max_length=100,
        #Se agregan a una lista las funciones que permiten hacer
        #validaciones personalizadas
        validators = [validar_caracteres_alfebeticos]
    )

    #Clase intermedia que se utiliza para configurar el comportamiento
    #del serializador
    class Meta:
        #Relaciono al serializador con el modelo correspondiente
        model = Curso 
        #Campos que quiero serializar del modelo
        fields = '__all__' 
        #fields = ['nombre','descripcion','modalidad']

    #VALIDACIONES PERSONALIZADAS
    # se crean funciones con el prefijo validate_ seguido del nombre
    # del campo que quiero validar, recibe un parametro value
    def validate_cost(self,value):
        if value < 0:
            #Lanzar una excepcion indicando el error que quiero controlar
            raise serializers.ValidationError('Validacion personalizada, el costo no puede ser negativo.')
        if value > 90000:
            raise serializers.ValidationError('El costo no puede superar los $90.000')
        return value
    
    def validate_start_date(self,value):
        """
        Valido que la fecha inicio no pueda ser menor a la de hoy
        """
        if value < date.today():
            raise serializers.ValidationError('La fecha de inicio no puede ser anterior a hoy.')
        
        return value


    #VALIDACION VARIOS CAMPOS A MISMA VEZ
    def validate(self,data):
        """
            data es un diccionario que contiene los campos y los valores que recibe
        """
        if data['level']=='Básico' and data['cost'] > 10000:
            raise serializers.ValidationError(
                {'cost':'Los cursos básico no puden superar los $10.000'}
            )

        return data

#Es posible definifir mas de un serializador para un mismo Modelo
class CursoReadSerializer(serializers.ModelSerializer):
    """
        Serializado de curso para operaciones lectura
    """
    #Serializadores anidados
    modulos =  ModuloSerializer(many=True,read_only=True)

    class Meta:
        model = Curso
        fields = ['id','name','image','level','modulos','description','start_date']
        #Profundidad de la serializacion teniendo en cuenta las relaciones
        #Recomendacion no usar depth > 1
        #depth = 1
        
class EstudianteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Estudiante
        fields = ['id','nombre','apellido','email','legajo','activo']

class InscripcionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inscripcion
        fields = '__all__'

    def validate(self, data):
        estudiante_data = data.get('estudiante')
        curso_data = data.get('curso')

        #No hacer inscripciones a estudiantes inactivos
        if not estudiante_data.activo:
            raise serializers.ValidationError(
                'No se puede inscribir a un estudiante inactivo.'
            )
        
        #Evitar inscripciones duplicadas
        #busco inscripcion con el ORM de Inscripcion en base al filtro de estudiante y curso
        existe_inscripcion = Inscripcion.objects.filter(
            estudiante= estudiante_data,
            curso = curso_data
        ).exists()  #exists() devuelve true/false
        if existe_inscripcion:
            raise serializers.ValidationError(
                'El estudiante ya registra una inscripción al curso'
            )
        
        return data

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    #classmethod se utiliza para definir un metodo que pertenece a la clase y
    # no a la instancia se puede llamar sin crear una instancia de la clase
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar claims personalizados
        token['email'] = user.email
        token['first_name'] = getattr(user, 'first_name', None)  # campo personalizado
        token['is_staff'] = getattr(user, 'is_staff', None)  # campo personalizado    
        return token
