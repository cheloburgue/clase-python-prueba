from django.shortcuts import render
from .models import Curso, Profesor
from django.http import HttpResponse
from .forms import CursoForm
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

def cursoFormulario(request):
    if request.method=="POST":
        #nombre = request.POST["nombre"] #Trae el contenido de lo que haya puesto en el id del input del html de cursoFormulario
        #comision = request.POST["comision"]
        form=CursoForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data #Muestra un diccionario con los datos del form. Convierte form en un dicc
            #print(info)
            #exit()
            nombre = info["nombre"]
            comision = info["comision"]
            curso = Curso(nombre=nombre, comision = comision)
            curso.save()
            return render(request, "AppCoder/cursoFormulario.html", {"mensaje": "Curso creado"})
        return render(request, "AppCoder/cursoFormulario.html", {"mensaje": "Datos Invalidos"})

        #creo un objeto curso y guardo en la db
        #curso = Curso(nombre=nombre,comision=comision)
        #curso.save()
        
    else:
        formulario_curso = CursoForm() # creo un objeto form
        return render(request, "AppCoder/cursoFormulario.html", {"formulario":formulario_curso})

def estudiantes(request):
    return render(request, "AppCoder/estudiantes.html")

def cursos(request):
    cursos = Curso.objects.all()
    return render(request, "AppCoder/cursos.html", {"cursos": cursos})

def entregables(request):
    return render(request, "AppCoder/entregables.html")