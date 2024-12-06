from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import index, agregar_vehiculo, listar_vehiculos

urlpatterns = [
    path('', index, name='index'),
    path('vehiculo/add/', agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculo/list/', listar_vehiculos, name='listar_vehiculos'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Vista para iniciar sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Vista para cerrar sesión
]
