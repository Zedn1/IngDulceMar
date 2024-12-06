from django.db import models
"""
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    fecha_lanzamiento = models.DateField()
    
    def __str__(self):
        return self.titulo
"""

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[
        ('Pasteles', 'Pasteles'),
        ('Panadería', 'Panadería'),
        ('Bebidas', 'Bebidas'),
        ('Otros', 'Otros'),
    ])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_en_stock = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def actualizar_stock(self, cantidad, es_entrada=True):
        """Actualiza el stock según el tipo de movimiento."""
        if es_entrada:
            self.cantidad_en_stock += cantidad
        else:
            self.cantidad_en_stock -= cantidad
        self.save()

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.tipo == 'Salida' and self.cantidad > self.producto.cantidad_en_stock:
            raise ValueError('No hay suficiente stock para realizar esta salida.')
        super().save(*args, **kwargs)
        self.producto.actualizar_stock(self.cantidad, es_entrada=self.tipo == 'Entrada')

class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ('Pendiente', 'Pendiente'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]
    cliente = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    productos = models.ManyToManyField(
        Producto,
        through='DetallePedido',  # Relación intermedia para incluir cantidades
    )
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def calcular_precio_total(self):
        """Calcula el precio total del pedido."""
        self.precio_total = sum(
            detalle.cantidad * detalle.producto.precio_unitario
            for detalle in self.detallepedido_set.all()
        )
        self.save()

    def __str__(self):
        return f"Pedido #{self.id} - {self.estado}"

class PedidoProveedor(models.Model):
    ESTADO_PEDIDO = [
        ('Pendiente', 'Pendiente'),
        ('Recibido', 'Recibido'),
        ('Cancelado', 'Cancelado'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido Proveedor #{self.id} - {self.estado}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.cantidad > self.producto.cantidad_en_stock:
            raise ValueError('No hay suficiente stock para este pedido.')
        super().save(*args, **kwargs)

class Gasto(models.Model):
    concepto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50, choices=[
        ('Ingredientes', 'Ingredientes'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Salarios', 'Salarios'),
        ('Otros', 'Otros'),
    ])

class Ingreso(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='ingreso')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Ingreso: ${self.monto} por Pedido #{self.pedido.id}"
