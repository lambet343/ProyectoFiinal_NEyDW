from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Lista de patrones de URL que mapean vistas a rutas específicas
urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para acceder al panel de administración de Django
    path('', views.mostrar_producto, name='mostrar_producto'),  # Página principal que muestra el catálogo de productos
    path('registro/', views.registrar_usuario, name='registrar_usuario'),  # Ruta para el registro de usuarios
    path('login/', views.iniciar_sesion, name='login'),  # Ruta para iniciar sesión
    path('logout/', views.logout_view, name='logout'),  # Ruta para cerrar sesión
    path('carrito/', views.ver_carrito, name='ver_carrito'),  # Página que muestra el carrito del usuario
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  
    # Ruta para agregar un producto específico al carrito (identificado por su ID)
    path('eliminar/<int:carrito_producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),  
    # Ruta para eliminar un producto específico del carrito (identificado por la relación carrito-producto)
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),  
    # Ruta para procesar un pedido a partir del carrito
    path('actualizar-cantidad/<int:carrito_producto_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),  
    # Ruta para actualizar la cantidad de un producto en el carrito
    path('resumen-compra/', views.resumen_compra, name='resumen_compra'),  
    # Página que muestra el resumen de la compra antes de confirmarla
    path('confirmar-compra/', views.confirmar_compra, name='confirmar_compra'),  
    # Ruta para confirmar una compra y procesar el pedido
    path('comparar/<int:producto_id>/', views.comparar, name='comparar'),  
    # Página para comparar un producto del catálogo con su paquete relacionado
    path('contacto/', views.contacto, name='contacto'),  
    # Ruta para mostrar el formulario de contacto y enviar consultas
]

# Agrega la configuración para servir archivos de medios en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Sirve archivos de imagen, video u otros medios subidos durante el desarrollo
