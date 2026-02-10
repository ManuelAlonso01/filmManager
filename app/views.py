from django.shortcuts import render, redirect, get_object_or_404
from .models import Movies
from django.contrib.auth.models import User
from .tools import generar_resumen
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    movies = request.user.movies.all()
    return render(request, 'app/index.html', {"movies": movies})

@login_required
def subir(request):
    if request.method == 'POST':
        user = request.user
        titulo = request.POST.get('titulo')
        img = request.POST.get('img')
        duration = request.POST.get('duration')
        descripcion = request.POST.get('descripcion')
        nota = request.POST.get('nota')

        Movies.objects.create(
            user=user,
            title=titulo,
            poster=img,
            duration_minutes=duration,
            descripcion=descripcion,
            calificacion=nota,
        )
        return redirect('index')

    return render(request, 'app/subir.html')


@login_required
def editar(request, id_pelicula):
    movie = get_object_or_404(
    Movies,
    id=id_pelicula,
    user=request.user
    )
    if request.method == 'POST':
        movie.title = request.POST.get('titulo')
        movie.poster = request.POST.get('img')
        movie.duration_minutes = request.POST.get('duration')
        movie.descripcion = request.POST.get('descripcion')
        movie.calificacion = request.POST.get('nota')
        movie.save()
        return redirect('index')
    return render (request, 'app/editar.html', {'pelicula': movie})

@login_required    
def resumen(request):
    data = generar_resumen(request)
    return render(request, 'app/resumen.html', {'data': data})


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(
                request,
                'app/login.html',
                {'error': 'Usuario o contraseña incorrectos'}
            )
    return render(request, 'app/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'app/register.html',
                {'error': 'El username ya esta en uso'}
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect('index')

    return render(request, 'app/register.html')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')
