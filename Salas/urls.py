from django.urls import path
from Salas import views

urlpatterns = [
    path('', views.home, name='Inicio'),
    path('reservar/', views.reservar, name='Reservar'),
    path('registrar_reservacion/', views.registrar_reservacion),
    path('edicion/<codigo>', views.edicion),
    path('editar/', views.editar),
    path('eliminar/<codigo>', views.eliminar),
    path('reservaciones/', views.reservaciones),
    path('reservacion/', views.reservacion),
    path('codigo/', views.codigo),
]
