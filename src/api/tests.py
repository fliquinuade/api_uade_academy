from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Curso, CustomUser
from rest_framework import status

# Create your tests here.
class CursoAPITestCase(APITestCase):
    """
    Clase de tests para probar los endpoints del CRUD de Cursos
    """

    def setUp(self):
        """
        setUp se ejecuta antes de cada caso de prueba y provee de información que podemos
        utilizar al correr los test.
        """
        #Crear un cliente de prueba para hacer las peticiones HTTP
        self.client = APIClient()

        #Crear un usuario para las pruebas que requieran autenticacion
        self.user = CustomUser.objects.create(
            email='test@test.com',
            password='password123.',
            first_name='Test',
            last_name='User'
        )

        #Creamos un atributo cursos_url para poder probar los endpoints
        self.cursos_url = '/api/cursos/'

        self.curso1 = Curso.objects.create(
            name='Python basico',
            description='Curso de pytho',
            course_number=1,
            cost = 10400.99,
            level = 'Básico',
            start_date='2025-10-14'
        )

        self.curso2 = Curso.objects.create(
            name='Python basico',
            description='Curso de pytho',
            course_number=1,
            cost = 10400.99,
            level = 'Básico',
            start_date='2025-10-14'
        )

    # GENERAR CASOS DE PRUEBA
    def test_obtener_lista_cursos(self):
        """
        Test 1: Verifica que se puede acceder a la lista de cursos por medio de GET /api/cursos/
        """

        #Hacemos la petición por GET a la ruta
        response = self.client.get(self.cursos_url)

        #Verificaciones
        #Verificar que la respuesta sea exitosa (codigo 200)
        with self.subTest("Verificando código de estado"):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Lista de cursos obtenida exitosamente - Código 200")

        #Verificacion de cantida de cursos de pruebas (los que creamos en el setUp)
        with self.subTest("Verificando cantidad de cursos"):
            self.assertGreaterEqual(len(response.data),4)
        print("Cantidad de cursos es correcta")



    def test_obtener_curso_inexistente(self):
        """
        Test 2: Verificar que obtenemos un error 404 al buscar un curso que no existe
        """
        url = f'{self.cursos_url}9999/'
        #Autenticar al usuario
        self.client.force_authenticate(user=self.user)

        #hacemos la peticion
        response = self.client.get(url)
        
        with self.subTest("Verificando codígo de estado 404"):
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Error 404 recibido")


        self.assertEqual(response.data['error'],'Curso no encontrado')
    




