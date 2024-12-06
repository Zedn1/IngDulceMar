from django.shortcuts import render
from django.db.models import Sum
from .models import Gasto, Ingreso, Pedido, PedidoProveedor

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

