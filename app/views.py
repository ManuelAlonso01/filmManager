from django.shortcuts import render, redirect
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
    
def resumen(request):
    data = generar_resumen()
    return render(request, 'app/resumen.html', {'data': data})