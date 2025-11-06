from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models.deletion import RestrictedError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Curso, Modulo
from .serializers import CursoSerializer, ModuloSerializer, CursoReadSerializer, ModuloWriteSerializer

from django.db.models import Q

#Permisos
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser
from utils.permission import TienePermisoModelo

#Paginacion
from rest_framework.pagination import PageNumberPagination
from utils.pagination import CustomPagination

#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Response as OpenAPIResponse


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

import logging

logger = logging.getLogger('api_uade')

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer



# Create your views here.
def inicio(request):
    mensaje = """<h1>AUDE ACADEMY</h1>"""
    return HttpResponse(mensaje)

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """
        Información general de la API de AUDE Academy
    """
    #Envio de correo en formato de texto plano
    # send_mail(
    #     subject='Email de bienvenida',
    #     message='Una prueba de envio de email 📨',
    #     from_email='jose.liquin@bue.edu.ar',
    #     recipient_list=['jliquin@uade.edu.ar'],
    #     fail_silently=False
    # )
    #Plantilla de email con html
    # html = '<h1>Test envio email</h1><p>Estoy probando formato HTML</p>'
    # text= 'Test envio email\nEstoy probando formato HTML'

    # email = EmailMultiAlternatives(
    #     subject='Envio email con HTML',
    #     body=text,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to=['jliquin@uade.edu.ar'],
    #     cc=[],
    #     bcc=[]
    # )

    # email.attach_alternative(html,"text/html")
    # email.send()

    response = {
        "message":"Bienvenido a la API de UADE Academy",
        "version": "2.5"
    }
    return JsonResponse(response)

from django.db import connection

@api_view(['GET'])
def search_users(request):
    query = request.GET.get('query','')
    #sql = "SELECT id, username FROM api_customuser WHERE username LIKE '%test%'"
    sql = "SELECT id, email FROM api_customuser WHERE email LIKE '%%%s%%';" % query
    print(f"SQL: {sql}")
    with connection.cursor() as c:
        c.execute(sql) # Ejecutando la consulta sql en la base
        rows = c.fetchall() # Extrar los datos de la consulta
    
    return Response(rows)

from .models import CustomUser

@api_view(['GET'])
def search_users_safe(request):
    query = request.GET.get('query','')

    users = CustomUser.objects.filter(
        Q(email__icontains=query) | Q(first_name__icontains=query)
    ).values('id','email')

    return Response({
        'count': users.count(),
        'result': list(users)
    })



# def api_cursos(request):
#     cursos = {
#         'nombre':'Python inicial',
#         'descripcion':'Un curso de python'
#     }
#     return JsonResponse(cursos)

class CursoAPIView(APIView):

    model = Curso
    permission_classes = [AllowAny]

    #Get hara referencia a poder gestionar peticiones HTTP del tipo GET
    @swagger_auto_schema(
        operation_description="Obtiene la lista de cursos. Mas texto explicativo",
        responses={200: CursoReadSerializer(many=True)}
    )
    def get(self, request):
        #Voy a buscar los cursos a mi base de datos
        """
        Aqui debera indicarle a la base que tiene que hacer
        SELECT * FROM api_cursos WHERE ;        
        """
        logger.info(f'{request.method} Solicitud iniciada para listar cursos')
        cursos = Curso.objects.all()
        logger.warning(f'Cursos: {cursos}')
        #cursos = Curso.objects.prefetch_related('modulos').all()

        # if modalidad_param and nombre_param:
        #     #SELECT * FROM Curso WHERE modalidad='virtual' AND nombre LIKE '%python%'
        #     cursos = Curso.objects.prefetch_related('modulos').filter(Q(modalidad__iexact=modalidad_param) & Q(nombre__icontains=nombre_param))
        # elif modalidad_param:
        #     cursos = Curso.objects.prefetch_related('modulos').filter(modalidad__iexact=modalidad_param)
        # elif nombre_param:
        #     cursos = Curso.objects.prefetch_related('modulos').filter(nombre__icontains=nombre_param)
        # else:
        #     cursos = Curso.objects.prefetch_related('modulos').all()

        # if nombre_param:
        #     cursos = Curso.objects.filter(nombre__icontains=nombre_param)
        #Filtros personalizados de busqueda
        #lt/lte -> menor / menor e igual
        #gt/gte -> mayor / mayor e igual
        #cursos = Curso.objects.filter(modalidad='presencial',cupo_maximo__lt=50)
        #__contains es estricto en minusculas/mayusculas
        #cursos = Curso.objects.filter(nombre__contains='python')
        #__icontains es indistinto en minusculas/mayusculas
        #cursos = Curso.objects.filter(nombre__icontains='python')
        #__exact / __iexact = validacion estrica del contenido
        #__startswith / __istartswith -> que comience por un valor
        #cursos = Curso.objects.filter(nombre__startswith='Curso')
        #__endswith / __iendswith -> finaliza por un valor
        #cursos = Curso.objects.filter(nombre__iendswith='python')
        #Utilizar el Serializador para convertir a una representacion JSON
        #many=True indica que estamos serializando una lista de objetos

        #Implementacion de paginacion
        # cursos = Curso.objects.all()
        # paginator = PageNumberPagination()
        # paginator.page_size = 10 # Configura la cantidad de elementos por pagina

        # paginator = CustomPagination() #Mi paginación personalizada
        # paginated_queryset = paginator.paginate_queryset(cursos,request)
        # serializer = CursoReadSerializer(paginated_queryset, many=True)

        # #Devolver la lista serializada como una respusta JSON al cliente
        # return paginator.get_paginated_response(serializer.data)


        level_param = request.query_params.get('level',None)
        name_param = request.query_params.get('name',None)
        filtros = Q()

        if level_param:
            filtros &= Q(level__iexact=level_param)
        if name_param:
            filtros &= Q(name__icontains=name_param)

        cursos = Curso.objects.filter(filtros) if filtros else Curso.objects.all()
        serializer = CursoReadSerializer(cursos, many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    @swagger_auto_schema(
        operation_description="API para crear un nuevo curso",
        request_body=CursoSerializer,
        responses={
                201: CursoSerializer,
                400: OpenAPIResponse(
                    description='Errores al crear curso',
                    examples={
                        "application/json":{
                            "nombre": ["Este campo no puede estar en blanco."],
                            "cupo_maximo": ["Debe ser un entero positivo."]
                        }
                    }
                ),
                403: "No tiene permisos para acceder al recurso"
            }

    )
    def post(self,request):
        #Recepciono los datos enviados en la solicitud - en formato de diccionario
        datos_peticion = request.data 
        #Serelizar los datos recibidos en base Serializador de curso
        serializer = CursoSerializer(data=datos_peticion)
        if serializer.is_valid():
            #los datos enviados son validos con respecto al modelo
            #tiene guardar esos datos en el modelo de curso
            #INSERT INTO cursos (campo1,campo2...) VALUES (valor1,valor2...)
            serializer.save()
            #Deberìa generar una respuesta al cliente
            respuesta = {
                'mensaje' : 'Curso creado exitosamente',
                'datos': serializer.data
            }
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #Sino pasa la validación respondo con los errores dectados
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CursoDetalleAPIView(APIView):

    model = Curso
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id_curso):
        #Ir a buscar en el modelo de Curso, el registro con pk=id_curso
        #Verificar si existe o no
        #Si existe deberia responder con los serializados del curso
        #Si no existe deberia responder con un error 404

        try:
            #SELECT * FROM Curso WHERE  primary_key=id_curso
            curso = Curso.objects.get(pk=id_curso)
        except Curso.DoesNotExist:
            return Response({'error':'El curso no existente'},status=status.HTTP_404_NOT_FOUND)
        #Serializa el curso encontrado
        serializer = CursoReadSerializer(curso)
        return Response(serializer.data)
    
    @swagger_auto_schema(auto_schema=None) #Quitan el endpoint de la documentacion
    def delete(self, request, id_curso):
        #Ir a buscar en el modelo de Curso, el registro con pk=id_curso
        #Verificar si existe o no
        #Si no existe deberia responder con un error 404
        #Si existe elimina el curso y responde OK
        try:
            #SELECT * FROM Curso WHERE  primary_key=id_curso
            curso = Curso.objects.get(pk=id_curso)
            serializer = CursoSerializer(curso)
            #DELETE FROM Curso WHERE primary_key=id_curso
            curso.delete()
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Curso.DoesNotExist:
            return Response({'error':'El curso no existente'},status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'error':'No se puede eliminar el curso porque tiene elementos relacionados'}
                            ,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,id_curso):    
        #Ir a buscar en el modelo de Curso, el registro con pk=id_curso
        #Verificar si existe o no
        #Si no existe deberia responder con un error 404
        #Si existe, serializar los datos enviados en el cuerpo de la peticion
        #Verifico si hay error en la serializacion
        #Si es valido, actualizo el cuso
        #Sino respondo con los errores encontrados
        try:
            #SELECT * FROM Curso WHERE  primary_key=id_curso
            curso = Curso.objects.get(pk=id_curso)
        except Curso.DoesNotExist:
            return Response({'error':'El curso no existente'},status=status.HTTP_404_NOT_FOUND)

        datos_peticion = request.data
        #Serializo
        serializer = CursoSerializer(curso,data=datos_peticion)
        if serializer.is_valid():
            #Si cumple las validaciones guardo el registro curso con sus cambios
            #UPDATE Cursos SET campo1=value1, ... WHERE pk=id_curso
            serializer.save()
            respuesta = {
                    'mensaje':'Curso Actualizado exitosamente.',
                    'data': serializer.data
                }
            return Response(serializer.data) #por defecto el codigo de status es 200
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ModuloAPIView(APIView):

    #Get hara referencia a poder gestionar peticiones HTTP del tipo GET
    def get(self, request):        
        #modulos = Modulo.objects.filter(nombre__icontains='React')
        # if duracion:
        #     modulos  = Modulo.objects.filter(duracion__lte=duracion,nombre__icontains='react')
        # else:
        #     modulos =  Modulo.objects.filter(nombre__icontains='python')

        #CONSULTA AVANZADAS SELECT_RELATED
        #1-> SELECT * FROM Modulo
        #2-> Recorre lista de modulos y busca informacion del curso asociado.
        # modulos = Modulo.objects.all()

        #SELECT m.nombre, m.duracion, c.nombre as nombre_curso FROM modulos m INNER JOIN cursos c ON c.id_curso = m.id_curso
        modulos = Modulo.objects.select_related('curso').all()
        #Si necesito filtar en base a un campo del modelo de curso
        #modulos_filtro = Modulo.objects.select_related('curso').filter(curso__modalidad__iexact='virtual',duracion__gte=3)

        serializer = ModuloSerializer(modulos, many=True)
        return Response(serializer.data)
    
    def post(self,request):        
        serializer = ModuloWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            respuesta = {
                'mensaje' : 'Modulo creado exitosamente',
                'datos': serializer.data
            }
            return Response(respuesta, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ModuloDetalleAPIView(APIView):

    def get(self,request,id_modulo):
        try:
            modulo = Modulo.objects.get(pk=id_modulo)
        except Modulo.DoesNotExist:
            return Response({'error':'El modulo no existente'},status=status.HTTP_404_NOT_FOUND)
        #Serializa el curso encontrado
        serializer = ModuloSerializer(modulo)
        return Response(serializer.data)
    
    def delete(self, request, id_modulo):
        try:
            modulo = Modulo.objects.get(pk=id_modulo)
            modulo.delete()
            return Response({'mensaje':'El módulo fue eliminado con exito.'},status=status.HTTP_200_OK)
        except Modulo.DoesNotExist:
            return Response({'error':'El módulo no existente'},status=status.HTTP_404_NOT_FOUND)
       

    def put(self, request,id_modulo):    
        try:
            modulo = Modulo.objects.get(pk=id_modulo)
        except Modulo.DoesNotExist:
            return Response({'error':'El modulo no existente'},status=status.HTTP_404_NOT_FOUND)
        serializer = ModuloSerializer(modulo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            respuesta = {
                    'mensaje':'Modulo Actualizado exitosamente.',
                    'data': serializer.data
                }
            return Response(respuesta) #por defecto el codigo de status es 200
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework.viewsets import ModelViewSet
from .serializers import EstudianteSerializer
from .models import Estudiante
from rest_framework.decorators import action

class EstudianteViewSet(ModelViewSet):
    #Especifico el serializador asociado
    serializer_class = EstudianteSerializer
    #Devolver todos los estudiantes
    #queryset = Estudiante.objects.all()
    queryset = Estudiante.objects.filter(activo=True)
    #Agregar permisos
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        #obtengo el parametro quety llamado nombre
        nombre = self.request.query_params.get('nombre',None)
        if nombre:
            return Estudiante.objects.filter(nombre__icontains=nombre)
        return Estudiante.objects.all()

    @action(detail=True, methods=['post'])
    def inactivar(self,request,pk):
        #Obtener el registro de un estudiante en base al id de la URL
        estudiante = self.get_object()
        estudiante.activo = False
        estudiante.save()
        return Response({'status':'Estudiante inactivo'})
    
    @action(detail=True, methods=['post'])
    def activar(self,request,pk):
        #Obtener el registro de un estudiante en base al id de la URL
        estudiante = self.get_object()
        estudiante.activo = True
        estudiante.save()
        return Response({'status':'Estudiante activo'})
    
