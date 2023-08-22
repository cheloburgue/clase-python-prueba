from django.shortcuts import render
from .models import Curso, Profesor
from django.http import HttpResponse
# Create your views here.

def crear_curso(request):
    nombre_curso="Corte y confeccion"
    comision_curso = 667791
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
    return render(request, "AppCoder/inicio.html")

def profesores(request):
    profesores = Profesor.objects.all()
    return render(request, "AppCoder/profesores.html", {"profes": profesores})

def estudiantes(request):
    return render(request, "AppCoder/estudiantes.html")

def cursos(request):
    cursos = Curso.objects.all()
    return render(request, "AppCoder/cursos.html", {"cursos": cursos})

def entregables(request):
    return render(request, "AppCoder/entregables.html")