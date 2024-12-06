from django.shortcuts import render, redirect
from .forms import VehiculoForm
from .models import Vehiculo
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django import forms

# Formulario de registro de usuario
class RegistroUsuarioForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# Vista principal
def index(request):
    return render(request, 'index.html')

@login_required
def mi_vista(request):
    context = {
        'puede_agregar_vehiculo': request.user.has_perm('vehiculo.add_vehiculomodel'),
    }
    return render(request, 'nombre_de_tu_template.html', context)


# Vista para agregar un vehículo, con permisos requeridos
@permission_required('vehiculo.add_vehiculo', raise_exception=True)
def agregar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el vehículo en la base de datos
            return redirect('listar_vehiculos')  # Redirige al listado de vehículos
    else:
        form = VehiculoForm()

    return render(request, 'agregar_vehiculo.html', {'form': form})

# Vista para listar vehículos, solo accesible para usuarios autenticados
@login_required  # Solo los usuarios autenticados pueden acceder
def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()  # Recupera todos los vehículos
    
    # Clasifica los precios
    for vehiculo in vehiculos:
        if vehiculo.precio <= 10000:
            vehiculo.categoria_precio = 'Bajo'
        elif vehiculo.precio <= 30000:
            vehiculo.categoria_precio = 'Medio'
        else:
            vehiculo.categoria_precio = 'Alto'
    
    return render(request, 'listar_vehiculos.html', {'vehiculos': vehiculos})

# Asignar el permiso 'visualizar_catalogo' a los usuarios
def asignar_permiso_usuario(user):
    try:
        permiso = Permission.objects.get(codename='visualizar_catalogo')
        user.user_permissions.add(permiso)
    except Permission.DoesNotExist:
        # Si no existe el permiso, no hace nada o puedes manejar el error como prefieras
        pass

# Vista para registrar un nuevo usuario
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            asignar_permiso_usuario(user)
            return redirect('login')  # Redirige a la página de login
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registro.html', {'form': form})

