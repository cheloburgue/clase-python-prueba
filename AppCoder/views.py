from django.shortcuts import render
from .models import Curso, Profesor, Estudiante, Avatar
from django.http import HttpResponse
from .forms import CursoForm, ProfesorForm, RegistroUsuarioForm, UserEditForm, AvatarForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin # Restringe acceso a vistas basadas en clases
from django.contrib.auth.decorators import login_required # Para vistas basadas en funciones
# Create your views here.

def obtenerAvatar(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    if len(avatares)!=0:
        return avatares[0].imagen.url
    else:
        return "/media/avatars/avatarpordefecto.png" 

@login_required
def crear_curso(request):
    nombre_curso="Corte y confeccion"
    comision_curso = 667791
    print("Creando curso")
    curso=Curso(nombre=nombre_curso,comision=comision_curso)
    curso.save()
    respuesta = f"Curso creado -- {nombre_curso} - {comision_curso}"
    return HttpResponse(respuesta)

@login_required  # Decorador, requiere del login para poder utilizar esta opcion
def listar_cursos(request):
    cursos = Curso.objects.all() # Traigo todos los objetos del modelo curso (de la db)
    respuesta = ""
    for curso in cursos:
        respuesta += f"{curso.nombre} - {curso.comision}<br>"
    return HttpResponse(respuesta) # Muestra el listado de todo lo que tengo en la base de datos

def inicio(request):
    return render(request, "AppCoder/inicio.html",{"avatar":obtenerAvatar(request)})

@login_required
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
    return render(request, "AppCoder/profesores.html", {"formulario": formulario_profesor, "profesores":profesores,"avatar":obtenerAvatar(request)})
@login_required
def eliminarProfesor(request,id):
    profesor = Profesor.objects.get(id=id)
    profesor.delete()
    profesores = Profesor.objects.all()
    formulario_profesor = ProfesorForm()
    mensaje = "Profesor Eliminado!"
    return render(request, "AppCoder/profesores.html", {"mensaje": mensaje,"formulario": formulario_profesor,"profesores": profesores,"avatar":obtenerAvatar(request)})
@login_required
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
            return render(request, "AppCoder/profesores.html", {"mensaje":mensaje, "formulario": formulario_profesor, "profesores": profesores,"avatar":obtenerAvatar(request)})

    else:
        formulario_profesor = ProfesorForm(initial={"nombre":profesor.nombre,"apellido":profesor.apellido,
                                                    "email":profesor.emails,"profesion":profesor.profesion})
        return render(request,"AppCoder/editarProfesor.html", {"formulario":formulario_profesor,"profesor":profesor,"avatar":obtenerAvatar(request)} )

class EstudianteList(ListView): # Hereda de LoginRequiredMixin, no se pueden usar sin registrase previamente
    model = Estudiante
    template_name = "AppCoder/estudiantes.html"

class EstudianteCreacion(LoginRequiredMixin, CreateView):
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

@login_required
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
            return render(request, "AppCoder/cursos.html", {"mensaje": "Curso creado","formulario":formulario_curso,"avatar":obtenerAvatar(request) })
        return render(request, "AppCoder/cursos.html", {"mensaje": "Datos Invalidos"})

        #creo un objeto curso y guardo en la db
        #curso = Curso(nombre=nombre,comision=comision)
        #curso.save()
        
    else:
        formulario_curso = CursoForm() # creo un objeto form
        return render(request, "AppCoder/cursos.html", {"formulario":formulario_curso,"avatar":obtenerAvatar(request)})

def estudiantes(request):
    avatar = obtenerAvatar(request)
    return render(request, "AppCoder/estudiantes.html",{"avatar":avatar})

def entregables(request):
    return render(request, "AppCoder/entregables.html",{"avatar":obtenerAvatar(request)})

# Busqueda por comision
def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html",{"avatar":obtenerAvatar(request)})

def buscarDatos(request):
    comision = request.GET["comision"]
    if comision !="":
        #Filtra por la comision del numero que me ingresaron por formulario
        cursos = Curso.objects.filter(comision=comision) # filter(comision__icontains=comision) busqueda por LIKE
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos":cursos,"avatar":obtenerAvatar(request)})
    else:
        return render(request, "AppCoder/resultadosBusqueda.html", {"mensaje":"No se ingresaron datos!"})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            info = form.cleaned_data # Copia la info del form y lo trae como un diccionario.
            user = info["username"]
            clave = info ["password"]
            #Verifica si el usuario existe, si existe devuelve el user, sino devuelve None
            usuario = authenticate(username = user, password = clave) 
            if usuario is not None:
                login(request, usuario)
                return render(request, "AppCoder/inicio.html",{"mensaje":f"Usuario {user} logueado correctamente","avatar":obtenerAvatar(request)})
        else:
            return render(request,"AppCoder/login.html", {"formulario":form, "mensaje":"Datos invalidos"})
        
    else: #Muestro formulario de login
        form = AuthenticationForm()
        return render(request, "AppCoder/login.html",{"formulario":form})
    
def register(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            nombre_usuario = info["username"]
            form.save()
            return render(request, "AppCoder/inicio.html", {"mensaje": f"Usuario {nombre_usuario} creado correctaente"})
        else:
            return render(request, "AppCoder/inicio.html", { "formulario": form, "mensaje": "Datos invalidos"})
    else:
        form = RegistroUsuarioForm()
        return render(request,"AppCoder/register.html", {"formulario":form})
    
@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            usuario.email = info["email"]
            usuario.password1 = info["password1"]
            usuario.password2 = info["password2"]
            usuario.first_name = info["first_name"] 
            usuario.last_name = info["last_name"]
            usuario.save()
            return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {usuario.username} editado correctamente"})
        else:
            return render(request, "AppCoder/editarPerfil.html",{"formulario":form, "nombreusuario":usuario.username, "mensaje":"Datos invalidos" })
    else:
        form = UserEditForm(instance=usuario)
        return render(request, "AppCoder/editarPerfil.html",{"formulario":form,"nombreusuario":usuario.username,"avatar":obtenerAvatar(request)})
    
@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES) #Traigo request.FILES porque se que tiene archivos
        if form.is_valid():
            avatar = Avatar(user = request.user, imagen = request.FILES["imagen"]) #Antes de guardarlo tengo que hacer algo
            #Busco si ya tengo un avatar cargado y si tengo lo borro. De esta manera siempre tengo 1 solo avatar por usuario
            avatarViejo = Avatar.objects.filter(user=request.user)
            if len(avatarViejo)>0 :
                avatarViejo[0].delete()
            avatar.save()
            return render(request, "AppCoder/inicio.html", {"mensaje": f"Avatar agregado correctamente", "avatar":obtenerAvatar(request)})
        else:
            return render(request, "AppCoder/agregarAvatar.html",{"formulario":form, "usuario": request.user, "mensaje":"Error al agregar el avatar"})
    else:
        form = AvatarForm()
        return render(request, "AppCoder/agregarAvatar.html", {"formulario":form, "usuario": request.user, "avatar":obtenerAvatar(request)})    