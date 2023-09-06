from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

#Creo un form apartir de una clase de django

class CursoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    comision = forms.IntegerField()

class ProfesorForm(forms.Form):
    # los campos del form son los mismos que el model
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    email = forms.EmailField()
    profesion = forms.CharField(max_length=50)

class RegistroUsuarioForm(UserCreationForm): #Hereda de un formn de creacion
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput) # Pone en el campo los ****
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta: #subclase dentro de RegistroUsuarioForm
        model = User #Django ya trae el modelo de User
        fields = ["username","email","password1","password2"]
        help_texts = { k:"" for k in fields} # Borra los help texts del formulario, el texto que esta debajo de los inputs

class UserEditForm(UserCreationForm):

    email = forms.EmailField(label="Email Usuario")
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Modificar Nombre")
    last_name = forms.CharField(label="Mofificar Apellido")

    class Meta:
        model = User
        fields = ["email","password1","password2","first_name","last_name"]
        help_texts = { k:"" for k in fields} 

class AvatarForm(forms.Form):
    imagen = forms.ImageField(label="Imagen")


