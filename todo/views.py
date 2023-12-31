from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import ToDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo/home.html')

def signup_usr(request):
    if request.method == 'GET':
        return render(request, 'todo/signupUsr.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupUsr.html', {'form':UserCreationForm(),'error':'такое имя уже существует'})
        else:
            return render(request, 'todo/signupUsr.html', {'form':UserCreationForm(),'error':'пароли не совпадают'})

def login_usr(request):
    if request.method == 'GET':
            return render(request, 'todo/loginUsr.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginUsr.html', {'form':AuthenticationForm(), 'error': "Логин или пароль неверны"})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logout_usr(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

# to do 
@login_required
def currenttodos(request):
    todos = ToDo.objects.filter(user=request.user, datacompleted__isnull=True).order_by('-created')
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = ToDo.objects.filter(user=request.user, datacompleted__isnull=False).order_by('-datacompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')

        except ValueError:
            return render(request, 'todo/view.html', {'form':todo, 'error':'неверно заполненое поле'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datacompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
    
@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/createTodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createTodo.html', {'form':TodoForm(), 'error':'неверно заполненое поле'})

