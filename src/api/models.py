from django.db import models

# Create your models here.
class Estudiante(models.Model):    
    nombre = models.CharField(max_length=100, verbose_name="Nombre") #verbose_name alias como utilzan en formularios
    apellido = models.CharField(max_length=50) #tamaño maximo caracteres= 50
    legajo = models.IntegerField(unique=True) #Es unico
    email = models.EmailField(null=True,max_length=50) #Puede ser null
    activo = models.BooleanField(default=True) #Los registros se creen con valor True por defecto

    def __str__(self):
        return f"{self.nombre}, {self.apellido} "

#RELACION ONE-TO-ONE ENTRE MODELOS
class EstudiantePerfil(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    biografia = models.TextField(null=True)
    recibe_novedades = models.BooleanField(default=True)

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True)
    nro_curso = models.IntegerField()
    cupo_maximo = models.PositiveIntegerField(default=50) #Entero positivo
    #Decimal con cantidad maxima de digitos y cantidad de parte decimal
    costo = models.DecimalField(max_digits=8,decimal_places=2,null=True) 
    url_info = models.URLField(null=True,max_length=150)
    #Generar un campo charfield con opciones para su cargar
    modalidad = models.CharField(
        max_length=20,
        choices=[
            ('virtual', 'Virtual'),
            ('presencial', 'Presencial'),
            ('hibrida','Híbrida')
        ],
        default='virtual',
        null=True
    )    

    def __str__(self):
        return f"{self.nombre} - {self.nro_curso}"

class Modulo(models.Model):
    #Relacion one-to-many
    curso = models.ForeignKey(
                Curso,
                on_delete=models.CASCADE,
                related_name='modulos'
            )
    nombre = models.CharField(max_length=100)
    duracion = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.curso.nombre}"

#ESTABLECIENDO UNA RELACION MANY-TO-MANY POR MEDIO DE UN MODELO INTERMEDIO
class Inscripcion(models.Model):
    #ONE-TO-MANY
    estudiante = models.ForeignKey(Estudiante,on_delete=models.RESTRICT)
    #ONE-TO-MANY
    curso = models.ForeignKey(Curso, on_delete=models.RESTRICT)
    fecha_inscripcion = models.DateField(auto_now_add=True) # Tome la fecha de creación por defecto
