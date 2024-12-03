import json
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Producto, Carrito, CarritoProducto, Pedido, Paquete
from .forms import RegistroUsuarioForm, ContactForm

# Vista para comparar un producto con su paquete relacionado
def comparar(request, producto_id):
    # Obtiene el producto específico del catálogo
    producto = Producto.objects.get(id=producto_id)
    # Obtiene el paquete relacionado al producto (si existe)
    paquete = producto.paquete
    # Renderiza la página de comparación con el producto y su paquete
    return render(request, 'comparar.html', {'producto': producto, 'paquete': paquete})

# Vista para mostrar el catálogo de productos
def mostrar_producto(request):
    # Obtiene todos los productos disponibles en el catálogo
    productos = Producto.objects.all()

    # Búsqueda por nombre del producto (si se proporciona una palabra clave)
    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(nombre__icontains=query)

    # Filtro por categoría del producto
    categoria = request.GET.get('categoria', '')
    if categoria:
        productos = productos.filter(categoria__icontains=categoria)

    # Filtro por rango de precios (mínimo y máximo)
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)  # Filtra productos con precio >= precio mínimo
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)  # Filtra productos con precio <= precio máximo

    # Carga paquetes relacionados desde un archivo JSON
    with open('scripts/paquetes.json', 'r', encoding='utf-8') as f:
        paquetes = json.load(f)

    # Renderiza la página del catálogo con productos, filtros y paquetes
    return render(request, 'catalogo.html', {
        'productos': productos,
        'paquetes': paquetes,
        'query': query,
        'categoria': categoria,
        'precio_min': precio_min,
        'precio_max': precio_max
    })

# Vista para mostrar los productos en el carrito de compras
@login_required
def ver_carrito(request):
    # Obtiene o crea el carrito asociado al usuario actual
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    # Obtiene los productos dentro del carrito
    productos = CarritoProducto.objects.filter(carrito=carrito)
    # Renderiza la página del carrito con los productos listados
    return render(request, 'ver_carrito.html', {'productos': productos})

# Vista para agregar productos al carrito de compras
@login_required
def agregar_al_carrito(request, producto_id):
    # Obtiene el producto por su ID
    producto = Producto.objects.get(id=producto_id)
    # Obtiene o crea el carrito asociado al usuario actual
    carrito, created = Carrito.objects.get_or_create(user=request.user)

    # Obtiene la cantidad seleccionada desde el formulario (por defecto, 1)
    cantidad = int(request.POST.get('cantidad', 1))
    # Valida que haya suficiente stock para la cantidad solicitada
    if cantidad > producto.stock:
        messages.error(request, f"No hay suficiente stock de {producto.nombre}. Solo quedan {producto.stock} unidades.")
        return redirect('ver_carrito')

    # Verifica si el producto ya está en el carrito
    carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        # Si ya existe, incrementa la cantidad
        carrito_producto.cantidad += cantidad
    else:
        # Si no existe, lo agrega con la cantidad seleccionada
        carrito_producto.cantidad = cantidad
    carrito_producto.save()

    # Muestra un mensaje de éxito al usuario
    messages.success(request, f"{producto.nombre} ha sido agregado al carrito.")
    return redirect('ver_carrito')

# Vista para actualizar la cantidad de un producto en el carrito
@login_required
def actualizar_cantidad(request, carrito_producto_id):
    # Obtiene la relación entre el carrito y el producto por su ID
    carrito_producto = CarritoProducto.objects.get(id=carrito_producto_id)
    # Obtiene la nueva cantidad ingresada por el usuario
    cantidad = int(request.POST.get('cantidad', 1))
    # Valida que la nueva cantidad no exceda el stock disponible
    if cantidad > carrito_producto.producto.stock:
        messages.error(request, f"No hay suficiente stock de {carrito_producto.producto.nombre}.")
        return redirect('ver_carrito')

    # Actualiza la cantidad del producto en el carrito y guarda los cambios
    carrito_producto.cantidad = cantidad
    carrito_producto.save()

    # Muestra un mensaje indicando que la cantidad fue actualizada
    messages.success(request, f"Cantidad de {carrito_producto.producto.nombre} actualizada a {cantidad}.")
    return redirect('ver_carrito')
# Vista para eliminar un producto del carrito
@login_required
def eliminar_del_carrito(request, carrito_producto_id):
    # Obtiene la relación carrito-producto por su ID
    carrito_producto = CarritoProducto.objects.get(id=carrito_producto_id)
    # Elimina el producto del carrito
    carrito_producto.delete()
    # Redirige a la página del carrito después de eliminar el producto
    return redirect('ver_carrito')

# Vista para procesar un pedido
@login_required
def procesar_pedido(request):
    # Obtiene o crea el carrito asociado al usuario actual
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    # Verifica si ya existe un pedido para este carrito
    if Pedido.objects.filter(carrito=carrito).exists():
        # Si ya existe un pedido, redirige al usuario al carrito con un mensaje de error
        messages.error(request, "Este pedido ya fue procesado anteriormente.")
        return redirect('ver_carrito')

    # Crea un nuevo pedido basado en el carrito actual
    Pedido.objects.create(carrito=carrito)
    # Vacía el carrito después de procesar el pedido
    carrito.productos.clear()
    # Muestra un mensaje de éxito y redirige al carrito
    messages.success(request, "Pedido procesado exitosamente.")
    return redirect('ver_carrito')

# Vista para mostrar el resumen de compra
@login_required
def resumen_compra(request):
    # Obtiene o crea el carrito asociado al usuario actual
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    # Obtiene los productos en el carrito
    productos = CarritoProducto.objects.filter(carrito=carrito)
    # Calcula el total del carrito sumando el precio de cada producto por su cantidad
    total = sum(item.producto.precio * item.cantidad for item in productos)
    # Renderiza la página del resumen con los productos y el total
    return render(request, 'resumen_compra.html', {'productos': productos, 'total': total})

# Vista para confirmar una compra
@login_required
def confirmar_compra(request):
    # Obtiene o crea el carrito asociado al usuario actual
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    # Obtiene los productos en el carrito
    productos = CarritoProducto.objects.filter(carrito=carrito)

    # Solo procesa la compra si el método de la solicitud es POST
    if request.method == 'POST':
        for item in productos:
            # Verifica que haya suficiente stock para cada producto
            if item.producto.stock < item.cantidad:
                messages.error(request, f"Stock insuficiente para {item.producto.nombre}.")
                return redirect('mostrar_producto')  # Redirige al catálogo si hay stock insuficiente
            # Reduce el stock del producto según la cantidad comprada
            item.producto.stock -= item.cantidad
            item.producto.save()

        # Crea un pedido asociado al carrito actual
        Pedido.objects.create(carrito=carrito)
        # Vacía el carrito después de completar la compra
        carrito.productos.clear()
        # Muestra un mensaje de éxito y redirige al catálogo
        messages.success(request, "Compra realizada correctamente.")
        return redirect('mostrar_producto')
    # Si el método no es POST, redirige al carrito
    return redirect('ver_carrito')

# Vista para registrar nuevos usuarios
def registrar_usuario(request):
    # Procesa el formulario de registro si la solicitud es POST
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Crea un nuevo usuario pero no lo guarda automáticamente
            user = form.save(commit=False)
            # Asigna la contraseña al usuario y guarda los cambios
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Inicia sesión automáticamente después de registrarse
            login(request, user)
            return redirect('mostrar_producto')  # Redirige al catálogo después del registro
    else:
        # Si la solicitud no es POST, muestra un formulario vacío
        form = RegistroUsuarioForm()
    # Renderiza la página de registro con el formulario
    return render(request, 'registro.html', {'form': form})

# Vista para iniciar sesión
def iniciar_sesion(request):
    # Procesa el formulario de inicio de sesión si la solicitud es POST
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autentica al usuario y lo inicia sesión
            usuario = form.get_user()
            login(request, usuario)
            # Redirige al panel de administración si el usuario es superusuario, de lo contrario al catálogo
            return redirect('/admin/' if usuario.is_superuser else 'mostrar_producto')
    else:
        # Si la solicitud no es POST, muestra un formulario de inicio de sesión vacío
        form = AuthenticationForm()
    # Renderiza la página de inicio de sesión con el formulario
    return render(request, 'login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    # Finaliza la sesión del usuario actual y redirige al catálogo
    logout(request)
    return redirect('mostrar_producto')

# Vista para procesar el formulario de contacto
def contacto(request):
    # Procesa el formulario de contacto si la solicitud es POST
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Obtiene los datos del formulario
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']
            
            # Envía un correo al administrador con los detalles del mensaje
            send_mail(
                f"Consulta de {nombre}",  # Asunto del correo
                mensaje,  # Contenido del mensaje
                correo,  # Correo del remitente
                ['partypackfi343@gmail.com'],  # Correo destinatario (administrador)
                fail_silently=False,  # Genera una excepción si hay un error
            )
            # Muestra un mensaje de éxito y redirige al catálogo
            messages.success(request, "Mensaje enviado.")
            return redirect('mostrar_producto')
    else:
        # Si la solicitud no es POST, muestra un formulario de contacto vacío
        form = ContactForm()
    # Renderiza la página de contacto con el formulario
    return render(request, 'contacto.html', {'form': form})
