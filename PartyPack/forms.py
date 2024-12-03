from django import forms
from django.contrib.auth.models import User

# Formulario para registrar un nuevo usuario
class RegistroUsuarioForm(forms.ModelForm):
    # Campo para la contraseña (oculta al escribir)
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    # Campo para confirmar la contraseña (también oculta)
    password_confirmado = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        # Modelo base para el formulario (User de Django)
        model = User
        # Campos que se incluirán en el formulario
        fields = ['username', 'email']

    # Validación personalizada para confirmar que las contraseñas coinciden
    def clean_password_confirmado(self):
        # Obtiene las contraseñas ingresadas
        password = self.cleaned_data.get('password')
        password_confirmado = self.cleaned_data.get('password_confirmado')

        # Verifica si las contraseñas no coinciden y lanza un error si es el caso
        if password != password_confirmado:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        # Devuelve la contraseña confirmada si pasa la validación
        return password_confirmado

# Formulario para el contacto con el administrador del sitio
class ContactForm(forms.Form):
    # Campo para el nombre del remitente
    nombre = forms.CharField(max_length=100, label="Nombre")
    # Campo para el correo electrónico del remitente
    correo = forms.EmailField(label="Correo Electrónico")
    # Campo para el mensaje que se enviará
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")
