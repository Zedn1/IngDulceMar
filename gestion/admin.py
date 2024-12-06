from django.contrib import admin
from .models import Producto, MovimientoInventario, Pedido, DetallePedido, PedidoProveedor

admin.site.register(Producto)
admin.site.register(MovimientoInventario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(PedidoProveedor)
