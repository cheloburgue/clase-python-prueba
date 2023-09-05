from django.shortcuts import render
from .models import Curso, Profesor, Estudiante
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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
    #Pregunto si viene por post para guardar en la db
    if request.method == "POST":
        #tomo los valores del formulario del post
        form = ProfesorForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            profesor = Profesor(nombre=info["nombre"],apellido=info["apellido"],emails=info["email"],profesion=info["profesion"])
            profesor.save()
            mensaje = "Profesor creado"
        else:
            mensaje = "Datos invalidos"
        formulario_profesor = ProfesorForm()
        profesores = Profesor.objects.all()
        return render(request, "AppCoder/profesores.html", {"mensaje": mensaje ,"formulario":formulario_profesor,"profesores":profesores})
    else: 
        #si viene por get mostrame el form vacio
        formulario_profesor = ProfesorForm()
        profesores = Profesor.objects.all()
    #devuelve el form vacio en la vista hacia el template ,"profesores": profesores,"profesores": profesores
    return render(request, "AppCoder/profesores.html", {"formulario": formulario_profesor, "profesores":profesores})

def eliminarProfesor(request,id):
    profesor = Profesor.objects.get(id=id)
    profesor.delete()
    profesores = Profesor.objects.all()
    formulario_profesor = ProfesorForm()
    mensaje = "Profesor Eliminado!"
    return render(request, "AppCoder/profesores.html", {"mensaje": mensaje,"formulario": formulario_profesor,"profesores": profesores})

def editarProfesor(request,id):
    profesor = Profesor.objects.get(id=id)

    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            profesor.nombre = info["nombre"]
            profesor.apellido = info["apellido"]
            profesor.emails = info["email"]
            profesor.profesion = info["profesion"]
            profesor.save()
            mensaje = "Cambios Guardados!"
            profesores = Profesor.objects.all()
            formulario_profesor = ProfesorForm ()
            return render (request, "AppCoder/profesores.html", {"mensaje":mensaje, "formulario": formulario_profesor, "profesores": profesores})

    else:
        formulario_profesor = ProfesorForm(initial={"nombre":profesor.nombre,"apellido":profesor.apellido,
                                                    "email":profesor.emails,"profesion":profesor.profesion})
        return render(request,"AppCoder/editarProfesor.html", {"formulario":formulario_profesor,"profesor":profesor} )

class EstudianteList(ListView):
    model = Estudiante
    template_name = "AppCoder/estudiantes.html"

class EstudianteCreacion(CreateView):
    model = Estudiante
    success_url = reverse_lazy("estudiante_list") # donde se dirige cuando ya este cargado el estudiante
    fields = ["nombre","apellido","email"]

class EstudianteDetalle(DetailView):
    model = Estudiante
    template_name = "AppCoder/estudiante_detalle.html"

class EstudianteDelete(DeleteView):
    model = Estudiante
    success_url = reverse_lazy("estudiante_list")

class EstudianteUpdate(UpdateView):
    model = Estudiante
    success_url = reverse_lazy("estudiante_list")
    fields = ['nombre','apellido','email']

def cursos(request):
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
            formulario_curso = CursoForm()
            return render(request, "AppCoder/cursos.html", {"mensaje": "Curso creado","formulario":formulario_curso })
        return render(request, "AppCoder/cursos.html", {"mensaje": "Datos Invalidos"})

        #creo un objeto curso y guardo en la db
        #curso = Curso(nombre=nombre,comision=comision)
        #curso.save()
        
    else:
        formulario_curso = CursoForm() # creo un objeto form
        return render(request, "AppCoder/cursos.html", {"formulario":formulario_curso})

def estudiantes(request):
    return render(request, "AppCoder/estudiantes.html")

def entregables(request):
    return render(request, "AppCoder/entregables.html")

# Busqueda por comision
def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html")

def buscarDatos(request):
    comision = request.GET["comision"]
    if comision !="":
        #Filtra por la comision del numero que me ingresaron por formulario
        cursos = Curso.objects.filter(comision=comision) # filter(comision__icontains=comision) busqueda por LIKE
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos":cursos})
    else:
        return render(request, "AppCoder/resultadosBusqueda.html", {"mensaje":"No se ingresaron datos!"})