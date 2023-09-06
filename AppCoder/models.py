from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Curso(models.Model): #Clase Curso es un modelo
    nombre = models.CharField(max_length=50)
    comision = models.IntegerField()
    def __str__(self):
        return f"{self.nombre} - {self.comision}"

class Estudiante(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    def __str__(self):
        return f"{self.nombre} - {self.apellido}"

class Profesor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    emails = models.EmailField()
    profesion = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.nombre} - {self.apellido}"

class Entregable(models.Model):
    nombre = models.CharField(max_length=50)
    fecha_entrega = models.DateField()
    entregado = models.BooleanField()
    def __str__(self):
        return f"{self.nombre} - {self.fecha_entrega} - {self.entregado}"

class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatars")
    user = models.ForeignKey(User,on_delete=models.CASCADE, null = True, blank = True) #Usuario queda vinculado al avatar por clave foranea. Si eliminan el user, se borra
                                                                                         # el avatar por el CASCADE