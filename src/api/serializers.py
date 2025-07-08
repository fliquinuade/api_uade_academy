from rest_framework import serializers
from .models import Curso, Estudiante, Modulo

class ModuloSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modulo
        fields = ['nombre','duracion','curso']
        depth = 1


class CursoSerializer(serializers.ModelSerializer):
    """
        Serializado de curso para operaciones de crear/actualizar
    """
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
    def validate_costo(self,value):
        if value < 0:
            #Lanzar una excepcion indicando el error que quiero controlar
            raise serializers.ValidationError('Validacion personalizada, el costo no puede ser negativo.')
        return value

    #VALIDACION VARIOS CAMPOS A MISMA VEZ
    def validate(self,data):
        """
            data es un diccionario que contiene los campos y los valores que recibe
        """
        if data['modalidad']=='presencial' and data['cupo_maximo'] > 100:
            raise serializers.ValidationError(
                {'cupo_maximo':'El cupo máximo para cursos presenciales no puede ser mayor a 100'}
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
        fields = ['nombre','nro_curso','modalidad','modulos','cupo_maximo','costo']
        #Profundidad de la serializacion teniendo en cuenta las relaciones
        #Recomendacion no usar depth > 1
        #depth = 1
        
class EstudianteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Estudiante
        fields = ['id','nombre','apellido','email']
