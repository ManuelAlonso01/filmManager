from django.shortcuts import render, redirect, get_object_or_404
from .models import Movies
from django.contrib.auth.models import User
from .tools import generar_resumen
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.http import content_disposition_header
import datetime
from .pdf_export import generar_pdf_resumen
@login_required
def index(request):
    selected_year = _selected_year(request)
    selected_rating_order = request.GET.get('rating_order', '')
    if selected_rating_order not in ('desc', 'asc'):
        selected_rating_order = ''
    favorites_only = request.GET.get('favorites') == 'on'

    movies = request.user.movies.all()
    if selected_year is not None:
        movies = movies.filter(year=selected_year)
    if favorites_only:
        movies = movies.filter(favorite=True)
    if selected_rating_order == 'desc':
        movies = movies.order_by('-calificacion', 'pk')
    elif selected_rating_order == 'asc':
        movies = movies.order_by('calificacion', 'pk')

    years = request.user.movies.values_list('year', flat=True).distinct().order_by('-year')
    return render(request, 'app/index.html', {
        "movies": movies,
        "years": years,
        "selected_year": selected_year,
        "selected_rating_order": selected_rating_order,
        "favorites_only": favorites_only,
    })

@login_required
def subir(request):
    if request.method == 'POST':
        user = request.user
        titulo = request.POST.get('titulo')
        img = request.POST.get('img')
        duration = request.POST.get('duration')
        descripcion = request.POST.get('descripcion')
        nota = request.POST.get('nota')
        is_serie = request.POST.get('is_serie') == 'on'
        year = datetime.date.today().year
        Movies.objects.create(
            user=user,
            title=titulo,
            poster=img,
            duration_minutes=duration,
            descripcion=descripcion,
            calificacion=nota,
            is_serie=is_serie,
            year=year,
            favorite=request.POST.get('favorite') == 'on'
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
        movie.is_serie = request.POST.get('is_serie') == 'on'
        movie.year = request.POST.get('year')
        movie.favorite = request.POST.get('favorite') == 'on'
        movie.save()
        return redirect('index')
    return render (request, 'app/editar.html', {'pelicula': movie})

@login_required    
def resumen(request):
    data = generar_resumen(request)
    years = request.user.movies.values_list('year', flat=True).distinct().order_by('-year')
    return render(request, 'app/resumen.html', {
        'data': data,
        'years': years,
        'selected_year': _selected_year(request),
    })

@login_required
def resumen_pdf(request):
    selected_year = _selected_year(request)
    if selected_year is None:
        selected_year = "all"
    pdf = generar_pdf_resumen(
        generar_resumen(request),
        request.user.username,
        selected_year,
    )
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'Estadisticas de la coleccion de {request.user.username} {selected_year}.pdf'
    response['Content-Disposition'] = content_disposition_header(
        as_attachment=True,
        filename=filename,
    )
    return response


def _selected_year(request):
    year = request.GET.get('year')
    try:
        return int(year) if year else None
    except (TypeError, ValueError):
        return None


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
