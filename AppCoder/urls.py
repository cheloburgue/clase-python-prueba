from django.urls import path
from .views import *

urlpatterns =[
    path("",inicio, name="inicio"), #Cuando no tiene nada en la url caiga inicio
    path("crear_curso/",crear_curso),
    path("listar_cursos/",listar_cursos),   
    path("profesores/",profesores, name="profesores"), # name es para poder invocarlo desde el href en el html y redireccionar botones a distintas paginas
    path("estudiantes/",estudiantes, name="estudiantes"),
    path("cursos/",cursos, name="cursos"),
    path("entregables/",entregables, name="entregables"),
]