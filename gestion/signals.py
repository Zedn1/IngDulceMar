from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Pedido, Ingreso, MovimientoInventario, DetallePedido

@receiver(post_save, sender=Pedido)
def crear_ingreso_y_movimiento_si_completado(sender, instance, created, **kwargs):
    """
    Crea un ingreso y movimientos de inventario cuando el estado del pedido se marca como Completado.
    """
    # Verificar si el pedido está completado
    if instance.estado == "Completado":
        # Crear ingreso si no existe
        if not hasattr(instance, 'ingreso'):
            Ingreso.objects.create(
                pedido=instance,
                monto=instance.precio_total,
            )
        
        # Generar movimientos de inventario para cada producto del pedido
        observaciones = []
        for detalle in DetallePedido.objects.filter(pedido=instance):
            producto = detalle.producto_id
            cantidad = detalle.cantidad
            
            # Crear el movimiento de inventario para cada producto
            MovimientoInventario.objects.create(
                producto_id=producto,
                tipo="Salida",
                cantidad=cantidad,
                observaciones=f"Venta asociada al Pedido #{instance.id}",
            )
            observaciones.append(f"{cantidad} x {producto.nombre}")


@receiver(post_save, sender=Pedido)
def actualizar_stock_al_cambiar_estado(sender, instance, **kwargs):
    """
    Actualiza el stock de los productos asociados al pedido cuando su estado cambia.
    """
    # Si el estado es "Completado"
    if instance.estado == "Completado":
        # Se reduce el stock de los productos cuando el pedido se completa
        for detalle in DetallePedido.objects.filter(pedido=instance):
            producto = detalle.producto
            cantidad = detalle.cantidad
            producto.cantidad_en_stock -= cantidad
            producto.save()

    elif instance.estado == "Pendiente":
        # Si el pedido está pendiente, se reserva el stock (se reduce para que no se pueda vender)
        for detalle in DetallePedido.objects.filter(pedido=instance):
            producto = detalle.producto
            cantidad = detalle.cantidad
            producto.cantidad_en_stock -= cantidad
            producto.save()

    elif instance.estado == "Cancelado":
        # Si el pedido se cancela, se vuelve a sumar al stock de los productos
        for detalle in DetallePedido.objects.filter(pedido=instance):
            producto = detalle.producto
            cantidad = detalle.cantidad
            producto.cantidad_en_stock += cantidad
            producto.save()


@receiver([post_save, post_delete], sender=DetallePedido)
def actualizar_precio_total(sender, instance, **kwargs):
    pedido = instance.pedido
    pedido.calcular_precio_total()