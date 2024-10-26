from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TareaForm
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm})

    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, 
                     "error": "Usuario ya existe"
                     })

        return render(
            request,
            "signup.html",{
                "form": UserCreationForm, 
                "error": "Contraseña no coincide"
                })

@login_required
def tasks(request):
    tareas = Tarea.objects.filter(usuario=request.user, realizado__isnull=True)
    return render(request, "tasks.html", {'tareas': tareas})

@login_required
def tasks_realizada(request):
    tareas = Tarea.objects.filter(usuario=request.user, realizado__isnull=False).order_by
    ('- realizado')
    return render(request, "tasks.html", {'tareas': tareas})

@login_required
def crear_tarea(request):
    if request.method == 'GET':
        return render(request, 'crear_tarea.html', {
            'form' : TareaForm
        })
    else:
        try:
            form = TareaForm(request.POST)
            nueva_tarea= form.save(commit=False)
            nueva_tarea.usuario = request.user
            nueva_tarea.save()
            return redirect('tasks')   
        except ValueError:
            return render(request, 'crear_tarea.html', {
                'form' : TareaForm,
                'error' : 'Por favor escriba datos validos'
            }) 

@login_required            
def detalle_tarea(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Tarea, pk=task_id, usuario=request.user)
        form= TareaForm(instance=task)
        return render(request, 'detalle_tarea.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Tarea, pk=task_id, usuario=request.user)
            form = TareaForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'detalle_tarea.html', {'task': task, 'form': form, 
                'error':'Error actualizando la tarea'
                })

@login_required            
def realizada_tarea(request, task_id):
    task= get_object_or_404(Tarea, pk=task_id, usuario=request.user)
    if request.method == 'POST':
        task.realizado = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def eliminar_tarea(request, task_id):
    task= get_object_or_404(Tarea, pk=task_id, usuario=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
        
@login_required        
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
            })
    else:
        user= authenticate(
            request, username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": 'Usuario o contraseña son incorrectas'
                })
        else:
            login(request, user)
            return redirect('tasks') 
        
