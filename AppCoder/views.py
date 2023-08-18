from django.shortcuts import render
from .models import Curso
from django.http import HttpResponse
# Create your views here.

def crear_curso(request):
    nombre_curso="Programacion basica"
    comision_curso = 667788
    print("Creando curso")
    curso=Curso(nombre=nombre_curso,comision=comision_curso)
    curso.save()
    respuesta = f"Curso creado -- {nombre_curso} - {comision_curso}"
    return HttpResponse(respuesta)

def listar_cursos(request):
    cursos = Curso.objects.all() # Traigo todos los objetos del modelo curso (de la db)
    respuesta = ""
    for curso in cursos:
        respuesta += f"{curso.nombre} - {curso.comision}<br>"
    return HttpResponse(respuesta) # Muestra el listado de todo lo que tengo en la base de datos

def inicio(request):
    return render(request, "inicio.html")

def profesores(request):
    return render(request, "profesores.html")

def estudiantes(request):
    return render(request, "estudiantes.html")

def cursos(request):
    return render(request, "cursos.html")

def entregables(request):
    return render(request, "entregables.html")