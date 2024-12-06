from django.contrib import admin
from .models import Producto, MovimientoInventario, Pedido, DetallePedido, Gasto, Ingreso, PedidoProveedor

admin.site.register(Producto)
admin.site.register(MovimientoInventario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Gasto)
admin.site.register(Ingreso)
admin.site.register(PedidoProveedor)
