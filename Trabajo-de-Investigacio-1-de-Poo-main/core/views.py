from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, get_form_by_model_name
from core.models import Cargo, Departamento, TipoContrato, Empleado, Rol
from django.db.models import Q
from django.contrib import messages

MODELS = {
    'cargo': Cargo,
    'departamento': Departamento,
    'tipocontrato': TipoContrato,
    'empleado': Empleado,
    'rol': Rol,
}

# =========================
# VISTAS DE AUTENTICACIÓN
# =========================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('core:login')

# ======================
# VISTA PRINCIPAL
# ======================

def home(request):
    return render(request, 'home.html')

# ======================
# CRUD GENERICO
# ======================

@login_required
def list_nomina(request, model_name):
    model = MODELS.get(model_name)
    if not model:
        return HttpResponse("Modelo no encontrado", status=404)

    if model_name in ['empleado', 'rol'] and not request.user.is_staff:
        messages.error(request, "Acceso denegado: no tienes permiso para ver este contenido.")
        return redirect('home')

    query = request.GET.get('q', '').strip()

    objects = model.objects.all()
    
    if model_name == 'empleado' and query:
        objects = objects.filter(Q(nombre__icontains=query) | Q(cedula__icontains=query))
    elif model_name != 'empleado' and query:
        objects = objects.filter(descripcion__icontains=query)

    fields = [field.name for field in model._meta.fields if field.name != 'id']
    context = {
        'title': f'Listado de {model_name.capitalize()}',
        'objects': objects,
        'model_name': model_name,
        'fields': fields,
    }

    return render(request, 'nomina/list.html', context)

@login_required
def create_nomina(request, model_name):
    if not request.user.is_staff:
        return HttpResponse("Solo administradores pueden crear registros.", status=403)

    model = MODELS.get(model_name)
    form_class = get_form_by_model_name(model_name)

    if not model or not form_class:
        return HttpResponse("Modelo o formulario no encontrado", status=404)

    form = form_class(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('core:list_nomina', model_name=model_name)

    context = {
        'form': form,
        'title': f'Crear {model_name.capitalize()}',
        'model_name': model_name,
    }
    return render(request, 'nomina/create.html', context)

@login_required
def update_nomina(request, model_name, id):
    if not request.user.is_staff:
        return HttpResponse("Solo administradores pueden editar registros.", status=403)

    model = MODELS.get(model_name)
    form_class = get_form_by_model_name(model_name)

    if not model or not form_class:
        return HttpResponse("Modelo o formulario no encontrado", status=404)

    instance = get_object_or_404(model, pk=id)
    form = form_class(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('core:list_nomina', model_name=model_name)

    context = {
        'form': form,
        'title': f'Actualizar {model_name.capitalize()}',
        'model_name': model_name,
    }
    return render(request, 'nomina/create.html', context)

@login_required
def delete_nomina(request, model_name, id):
    if not request.user.is_staff:
        return HttpResponse("Solo administradores pueden eliminar registros.", status=403)

    model = MODELS.get(model_name)
    instance = get_object_or_404(model, pk=id)

    if request.method == 'POST':
        instance.delete()
        return redirect('core:list_nomina', model_name=model_name)

    context = {
        'object': instance,
        'title': f'Eliminar {model_name.capitalize()}',
        'model_name': model_name,
    }
    return render(request, 'nomina/delete.html', context)