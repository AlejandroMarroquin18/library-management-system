from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Formulario de creación de usuario personalizado que hereda de UserCreationForm.
# Se agrega un campo de correo electrónico obligatorio y se define el modelo y los campos que se utilizarán en el formulario. 
# Además, se sobrescribe el método save para asignar el rol por defecto de "CUSTOMER" al usuario creado.
class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        # Guardamos el usuario sin enviar aún a la base de datos
        user = super().save(commit=False)
        # Asignamos el rol por defecto de forma segura en el backend
        user.role = 'CUSTOMER'
        
        if commit:
            user.save()
        return user