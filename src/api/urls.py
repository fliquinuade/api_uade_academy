from django.urls import path
from . import views
#from views import inicio

urlpatterns = [
    path('otra_ruta/', views.inicio),
    path('info/', views.api_info),
    path('cursos/', views.CursoAPIView.as_view()),
    path('cursos/<int:id_curso>/', views.CursoDetalleAPIView.as_view()),
    path('modulos/',views.ModuloAPIView.as_view()),
    path('modulos/<int:id_modulo>/',views.ModuloDetalleAPIView.as_view())

]

