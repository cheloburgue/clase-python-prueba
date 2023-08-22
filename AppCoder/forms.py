from django import forms 

#Creo un form apartir de una clase de django

class CursoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    comision = forms.IntegerField()
