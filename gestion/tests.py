from django.test import TestCase
from .models import Producto, Pedido, DetallePedido, Ingreso, Gasto

class GestionTestCase(TestCase):
    def test_calculo_precio_total_pedido(self):
        producto = Producto.objects.create(nombre="Tarta", precio_unitario=10, cantidad_en_stock=50)
        pedido = Pedido.objects.create(estado='Pendiente')
        DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=5)
        pedido.calcular_precio_total()
        self.assertEqual(pedido.precio_total, 50)
