from django.contrib import admin
# Importa los modelos Producto y Paquete que han sido definidos en models.py
from .models import Producto, Paquete

# Registra el modelo Producto en el sitio de administración de Django para que sea accesible desde la interfaz de administración
admin.site.register(Producto)

# Registra el modelo Paquete en el sitio de administración de Django para que sea accesible desde la interfaz de administración
admin.site.register(Paquete)
