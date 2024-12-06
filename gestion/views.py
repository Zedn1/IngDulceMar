from django.shortcuts import render
from django.db.models import Sum
from .models import Gasto, Ingreso, Pedido, PedidoProveedor

# Create your views here.
def ingresos_y_gastos(request):
    ingresos = Ingreso.objects.aggregate(total_ingresos=Sum('monto'))['total_ingresos'] or 0
    gastos = Gasto.objects.aggregate(total_gastos=Sum('monto'))['total_gastos'] or 0
    balance = ingresos - gastos
    return render(request, 'gestion/ingresosYGastos.html', {
        'ingresos': ingresos,
        'gastos': gastos,
        'balance': balance,
    })

def pedidos(request):
    pedidos_pendientes = Pedido.objects.filter(estado='Pendiente')
    pedidos_realizados = Pedido.objects.filter(estado='Completado')
    return render(request, 'gestion/pedidos.html', {
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_realizados': pedidos_realizados,
    })

def pedidos_proveedores(request):
    pedidos = PedidoProveedor.objects.all().order_by('estado', 'fecha_creacion')
    return render(request, 'gestion/pedidosProveedores.html', {'pedidos': pedidos})

