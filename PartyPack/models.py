from django.db import models
from django.contrib.auth.models import User

# Modelo para los paquetes, representando una oferta o grupo de servicios
class Paquete(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del paquete
    descripcion = models.TextField()  # Descripción del paquete
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del paquete

    def __str__(self):
        return self.nombre  # Representación en texto del modelo (nombre del paquete)

# Modelo para los productos disponibles en el catálogo
class Producto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField()  # Descripción del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    stock = models.PositiveIntegerField()  # Cantidad disponible en inventario
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Imagen del producto
    disponibilidad = models.BooleanField(default=True)  # Indica si el producto está disponible
    paquete = models.ForeignKey(
        Paquete, 
        on_delete=models.CASCADE, 
        related_name="productos", 
        blank=True, 
        null=True
    )  # Relación opcional con un paquete
    categoria = models.CharField(max_length=100, blank=True, null=True)  # Categoría del producto

    def __str__(self):
        return self.nombre  # Representación en texto del modelo (nombre del producto)

# Modelo para el carrito de compras de un usuario
class Carrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario propietario del carrito
    productos = models.ManyToManyField(Producto, through='CarritoProducto')  # Relación con los productos a través de CarritoProducto

    def __str__(self):
        return f"Carrito de {self.user.username}"  # Representación del carrito con el nombre del usuario

# Modelo intermedio que conecta el carrito con los productos y su cantidad
class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)  # Relación con el carrito
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con el producto
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad de este producto en el carrito

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"  # Representación del producto con su cantidad

# Modelo para registrar pedidos realizados
class Pedido(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)  # Carrito asociado al pedido
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pedido
    estado = models.CharField(
        max_length=20, 
        default='Pendiente'
    )  # Estado del pedido: Pendiente, Enviado, etc.

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"  # Representación del pedido con su ID y estado
