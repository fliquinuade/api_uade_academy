from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager


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
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    course_number = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    #Decimal con cantidad maxima de digitos y cantidad de parte decimal
    cost = models.DecimalField(max_digits=8,decimal_places=2,null=True) 
    image = models.URLField(null=True,max_length=150)
    #Generar un campo charfield con opciones para su cargar
    level = models.CharField(
        max_length=20,
        choices=[
            ('Básico', 'Básico'),
            ('Intermedio', 'Intermedio'),
            ('Avanzado','Avanzado')
        ],
        default='Básico',
        null=True
    )    

    def __str__(self):
        return f"{self.name} - {self.course_number}"

class Modulo(models.Model):
    #Relacion one-to-many
    curso = models.ForeignKey(
                Curso,
                on_delete=models.CASCADE,
                related_name='modulos'
            )
    nombre = models.CharField(max_length=100)
    duracion = models.IntegerField()
    ficha = models.FileField(upload_to='modulos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.curso.name}"

#ESTABLECIENDO UNA RELACION MANY-TO-MANY POR MEDIO DE UN MODELO INTERMEDIO
class Inscripcion(models.Model):
    #ONE-TO-MANY
    estudiante = models.ForeignKey(Estudiante,on_delete=models.RESTRICT)
    #ONE-TO-MANY
    curso = models.ForeignKey(Curso, on_delete=models.RESTRICT)
    fecha_inscripcion = models.DateField(auto_now_add=True) # Tome la fecha de creación por defecto



# class CustomUser(AbstractUser):

#     phone = models.CharField(max_length=20,blank=True,null=True)
#     address = models.CharField(max_length=150,null=True,blank=True)
#     birth_date = models.DateField(blank=True,null=True)
#     notes = models.TextField(null=True,blank=True)

#La clase em la que voy a poder definir ciertos comportamientos personalizado
#para las funciones como por ejemplo create_user
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_field):
        #DOMAINS = ('gmail.com','uade.edu.ar')
        if not email :
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_field):
        extra_field.setdefault('is_staff',True)
        extra_field.setdefault('is_superuser',True)
        return self.create_user(email,password, **extra_field)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=15, null=True,blank=True)

    #Setear el manejador del ORM para CustomUser
    objects = CustomUserManager()

    #indico cual será el campo username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email



