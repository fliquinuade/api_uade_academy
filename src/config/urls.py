"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#DEPENDENCIAS DE YASG
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.views import CustomTokenObtainPairView

from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="API de UADE Academy",
        default_version='v1.1',
        description='Documentación general del proyecto API REST de UADE ACADEMY'
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    #Endpoints para documentacion
    path('documentacion_swagger/', schema_view.with_ui('swagger',cache_timeout=0)),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0)),
    #Endpoint para obtener el token - Funcion por POST
    #path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/', CustomTokenObtainPairView.as_view()),
    #Endpoint para refrescar el token 
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('admin/', admin.site.urls),
     # estoy asociando con un prefijo 'api/' a las rutas
     # definidas en el archivo url.py de la aplicacion 'api'
    path('api/',include('api.urls'))
]

#Habilitamos URLS para los archivos media del proyecto
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

