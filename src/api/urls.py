from django.urls import path
from . import views
#from views import inicio
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#Genera rutas de forma dinamica en base al ViewSet
router.register(r'estudiantes',views.EstudianteViewSet, basename='estudiantes')


urlpatterns = [
    path('search_users/',views.search_users),
    path('search_users_safe/',views.search_users_safe),
    path('otra_ruta/', views.inicio),
    path('info/', views.api_info),
    path('cursos/', views.CursoAPIView.as_view()),
    path('cursos/<int:id_curso>/', views.CursoDetalleAPIView.as_view()),
    path('modulos/',views.ModuloAPIView.as_view()),
    path('modulos/<int:id_modulo>/',views.ModuloDetalleAPIView.as_view())
]

#Sumamos al listado de rutas, las generadas automaticamente por el router
urlpatterns += router.urls

