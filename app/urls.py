from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("subir/", views.subir, name="subir"),
    path("resumen/", views.resumen, name="resumen"),
    path("editar/<int:id_pelicula>", views.editar, name="editar"),
    path("accounts/login/", views.iniciar_sesion, name="login"),
    path("register/", views.register, name="register"),
    path("accounts/logout/", views.cerrar_sesion, name="logout"),
]