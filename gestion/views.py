from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.urls import reverse
from django.contrib import messages
from .models import Gasto, Ingreso, Pedido, Producto, PedidoProveedor, DetallePedido
from .forms import PedidoForm, DetallePedidoFormSet

# Create your views here.
def ingresos_y_gastos(request):
    ingresos = Ingreso.objects.all().order_by('-fecha')
    gastos = Gasto.objects.all().order_by('-fecha')
    ingresos_totales = Ingreso.objects.aggregate(total_ingresos=Sum('monto'))['total_ingresos'] or 0
    gastos_totales = Gasto.objects.aggregate(total_gastos=Sum('monto'))['total_gastos'] or 0
    balance = ingresos_totales - gastos_totales
    balance_clase = "positivo" if balance >= 0 else "negativo"
    return render(request, 'gestion/ingresosYGastos.html', {
        'ingresos_totales': ingresos_totales,
        'gastos_totales': gastos_totales,
        'balance': balance,
        'balance_clase': balance_clase,
        'ingresos_list': ingresos,
        'gastos_list': gastos,
    })

def pedidos(request):
    pedidos = Pedido.objects.all().order_by('estado')
    return render(request, 'gestion/pedidos.html', {
        'pedidos': pedidos,
    })

def pedidos_proveedores(request):
    pedidos = PedidoProveedor.objects.all().order_by('estado', 'fecha_creacion')
    return render(request, 'gestion/pedidosProveedores.html', {'pedidos': pedidos})


# Vista para crear un pedido
def crear_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        formset = DetallePedidoFormSet(request.POST)
        if pedido_form.is_valid() and formset.is_valid():
            pedido = pedido_form.save()
            formset.instance = pedido  # Asigna el pedido al formset
            formset.save()
            pedido.calcular_precio_total()  # Actualiza el precio total
            messages.success(request, 'Pedido creado exitosamente.')
            return redirect('gestion:pedidos')  # Cambia según tu URL
    else:
        pedido_form = PedidoForm()
        formset = DetallePedidoFormSet()
    return render(request, 'gestion/crear_pedido.html', {
        'pedido_form': pedido_form,
        'formset': formset
    })

# Vista para editar un pedido
def editar_pedido(request, id):
    productos = Producto.objects.all().order_by('nombre')
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST, instance=pedido)
        formset = DetallePedidoFormSet(request.POST, instance=pedido)
        if pedido_form.is_valid() and formset.is_valid():
            pedido.save()
            formset.save()
            pedido.calcular_precio_total()
            messages.success(request, 'Pedido actualizado exitosamente.')
            return redirect('gestion:pedidos')
    else:
        pedido_form = PedidoForm(instance=pedido)
        formset = DetallePedidoFormSet(instance=pedido)
    return render(request, 'gestion/editar_pedido.html', {
        'pedido_form': pedido_form,
        'formset': formset,
        'pedido': pedido,
        'productos': productos
    })

# Vista para eliminar un pedido
def eliminar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    if request.method == "POST":
        pedido.delete()
        messages.success(request, "Pedido eliminado exitosamente.")
        return redirect('gestion:pedidos')  # Cambia este nombre por la URL de la lista de pedidos
    return render(request, 'gestion/eliminar_pedidos.html', {'pedido': pedido})

def eliminar_producto(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    pedido = detalle.pedido
    detalle.delete()
    messages.success(request, f"Producto eliminado de pedido #{pedido.id}")
    return redirect('gestion:editar_pedido', id=pedido.id)
