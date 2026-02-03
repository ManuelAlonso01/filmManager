from django.shortcuts import render, redirect, get_object_or_404
from .models import Movies
from .tools import generar_resumen
# Create your views here.


def index(request):
    movies = Movies.objects.all()
    return render(request, 'app/index.html', {"movies": movies})

def subir(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        img = request.POST.get('img')
        duration = request.POST.get('duration')
        descripcion = request.POST.get('descripcion')
        nota = request.POST.get('nota')
        Movies.objects.create(
            title=titulo,
            poster=img,
            duration_minutes = duration,
            descripcion=descripcion,
            calificacion=nota,
        )
        return redirect('index')
    return render (request, 'app/subir.html')

def editar(request, id_pelicula):
    movie = get_object_or_404(Movies, id=id_pelicula)
    if request.method == 'POST':
        movie.title = request.POST.get('titulo')
        movie.poster = request.POST.get('img')
        movie.duration = request.POST.get('duration')
        movie.descripcion = request.POST.get('descripcion')
        movie.calificacion = request.POST.get('nota')
        movie.save()
        return redirect('index')
    return render (request, 'app/editar.html', {'pelicula': movie})
    
def resumen(request):
    data = generar_resumen()
    return render(request, 'app/resumen.html', {'data': data})