from .models import Movies
from django.db.models import Sum, Avg

def minutos_a_tiempo(minutos):
    dias = minutos // 1440
    horas = (minutos % 1440) // 60
    minutos_restantes = minutos % 60
    if minutos_restantes > 0:
        if horas > 0:
            if dias > 0:
                return f'{dias} dias, {horas} horas y {minutos_restantes} minutos'
            return f'{horas} horas y {minutos_restantes} minutos'
        return f'{minutos_restantes} minutos'

def generar_resumen():
    peliculas_vistas = Movies.objects.count()
    tiempo_invertido = Movies.objects.aggregate(Sum("duration_minutes"))['duration_minutes__sum']
    nota_media = Movies.objects.aggregate(Avg('calificacion'))['calificacion__avg']
    pelicula_mas_larga = Movies.objects.order_by("-duration_minutes").first()
    pelicula_mas_corta = Movies.objects.order_by("duration_minutes").first()
    top_mejores = Movies.objects.order_by("-calificacion")[:3]
    top_peores = Movies.objects.order_by("calificacion")[:3]
    data = {
        'peliculas_vistas': peliculas_vistas,
        'tiempo_invertido': minutos_a_tiempo(tiempo_invertido),
        'nota_media': round(nota_media, 2),
        'pelicula_mas_larga': pelicula_mas_larga.title,
        'pelicula_mas_corta': pelicula_mas_corta.title,
        'top_mejores': f"{top_mejores[0].title}, {top_mejores[1].title}, {top_mejores[2].title}",
        'top_peores': f"{top_peores[0].title}, {top_peores[1].title}, {top_peores[2].title}",
    }
    return data