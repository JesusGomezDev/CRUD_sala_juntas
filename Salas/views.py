from re import L
import re
from django.shortcuts import render, redirect, HttpResponse
from .models import Reservas
import random
import datetime
from django.db.models import Q

# Create your views here.


def home(request):
    hoy = datetime.datetime.now()
    lista_reservaciones = Reservas.objects.filter(
        fecha__gte=hoy).order_by('fecha')
    terminadas = Reservas.objects.filter(
        fecha__lte=hoy, final__lte=hoy)
    terminadas.delete()
    return render(request, "index.html", {"reservaciones": lista_reservaciones})


def reservar(request):
    return render(request, "reservar.html")


def registrar_reservacion(request):
    codigo = random.randint(1000, 9999)
    fecha = request.POST['fecha']
    inicio = request.POST['hora_inicio']
    final = request.POST['hora_final']
    sala = request.POST['sala_seleccionada']
    hora_final = datetime.datetime.strptime(final, '%H:%M')
    hora_inicial = datetime.datetime.strptime(inicio, '%H:%M')
    diferencia = abs(hora_final-hora_inicial)
    delta = datetime.timedelta(hours=2)
    reserva = Reservas.objects.create(
        codigo=codigo, fecha=fecha, inicio=inicio, final=final, sala=sala)

    libre = comprobacion(request, sala, fecha, hora_final, hora_inicial)

    return render(request, "Codigo.html", {'reserva': reserva, 'diferencia': diferencia, 'delta': delta, 'reservaciones': reservaciones, 'libre': libre})

# Esta es la función que se encarga de comprobar si una sala se encuentra disponible y retorna un valor boolean con True en caso de que esté disponible y con False en caso de que se encuentr ocupada dentro de ese mismo rango de tiempo


def comprobacion(request, sala, fecha, hora_final, hora_inicial):
    libre = True
    reservaciones = Reservas.objects.filter(sala=sala, fecha=fecha)
    i = hora_inicial.time()
    f = hora_final.time()
    for reserv in reservaciones:
        fin = reserv.final
        inic = reserv.inicio
        if (i >= inic and f <= fin or i <= inic and f >= fin or i >= inic and i <= fin or f >= inic and f <= fin):
            libre = True
        else:
            libre = False

    return libre


def codigo(request):
    return redirect('/')


def edicion(request, codigo):
    reserva = Reservas.objects.get(codigo=codigo)
    en_curso = False
    hoy = datetime.datetime.now()
    hoy_hora = hoy.time()
    hora_final = reserva.final
    hora_inicial = reserva.inicio
    fecha_reserva = reserva.fecha
    if hoy_hora >= hora_inicial and hoy_hora <= hora_final and fecha_reserva == hoy:
        en_curso = True
    else:
        en_curso = False
    return render(request, "edicion.html", {'reserva': reserva, 'en_curso': en_curso})


def editar(request):
    codigo = request.POST['codigo']
    fecha = request.POST['fecha']
    inicio = request.POST['hora_inicio']
    final = request.POST['hora_final']

    reserva = Reservas.objects.get(codigo=codigo)
    reserva.fecha = fecha
    reserva.inicio = inicio
    reserva.final = final
    reserva.save()

    return redirect('/')


def eliminar(request, codigo):
    reserva = Reservas.objects.get(codigo=codigo)
    reserva.delete()

    return redirect('/')


def reservaciones(request):
    return render(request, 'reservaciones.html')


def reservacion(request):
    aux = request.POST.get('codigo_txt')
    reserva = Reservas.objects.get(codigo=aux)
    if reserva:
        return render(request, "reservacion.html", {'reserva': reserva})
    else:
        return render(request, "fallo.html")
