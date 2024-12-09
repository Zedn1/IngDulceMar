from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from django.forms import modelformset_factory
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
        if pedido_form.is_valid():
            # Crear el pedido con los datos iniciales
            pedido = pedido_form.save(commit=False)
            pedido.precio_total = 0  # Inicializar con 0 ya que aún no tiene productos
            pedido.save()
            messages.success(request, 'Pedido creado exitosamente. Ahora puedes agregar productos.')
            # Redirigir a la vista de edición para agregar productos
            return redirect(reverse('gestion:editar_pedido', args=[pedido.id]))
    else:
        pedido_form = PedidoForm()
    
    return render(request, 'gestion/crear_pedido.html', {
        'pedido_form': pedido_form
    })

# Vista para editar un pedido y agregar productos
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    productos = Producto.objects.all().order_by('nombre')

    if request.method == 'POST':
        formset = DetallePedidoFormSet(request.POST, queryset=pedido.detallepedido_set.all())
        
        if formset.is_valid():
            # Diagnóstico de los datos validados
            for form in formset:
                print(f"Formulario válido: {form.cleaned_data}")
            
            # Si el formset es válido, procesamos los formularios
            with transaction.atomic():
                for form in formset:
                    # Ignorar formularios vacíos o no válidos
                    if not form.cleaned_data:
                        continue

                    # Eliminar los objetos DetallePedido marcados para eliminación
                    if form.cleaned_data.get('DELETE', False):
                        if form.instance.pk:  # Solo eliminar si ya existe
                            form.instance.delete()  # Eliminar el detalle del pedido
                        continue  # Continuar con el siguiente formulario

                    # Guardar los formularios válidos con el pedido asociado
                    detalle = form.save(commit=False)
                    detalle.pedido = pedido  # Asignar el pedido al detalle
                    detalle.save()

                # Actualizar el precio total del pedido
                pedido.calcular_precio_total()

            # Mensaje de éxito
            messages.success(request, 'Pedido actualizado exitosamente.')
            return redirect('gestion:pedidos')
        
        else:
            print("Errores en el formset:")
            print(formset.errors)  # Diagnóstico de errores en el formset

    else:
        formset = DetallePedidoFormSet(queryset=pedido.detallepedido_set.all())

    return render(request, 'gestion/editar_pedido.html', {
        'pedido': pedido,
        'formset': formset,
        'productos': productos,
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
