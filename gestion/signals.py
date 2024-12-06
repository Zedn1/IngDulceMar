from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido, Ingreso

@receiver(post_save, sender=Pedido)
def crear_ingreso_si_completado(sender, instance, **kwargs):
    """Crea un ingreso cuando el estado del pedido cambia a Completado."""
    if instance.estado == "Completado" and not hasattr(instance, 'ingreso'):
        Ingreso.objects.create(
            pedido=instance,
            monto=instance.precio_total,  # Se usa el precio total del pedido
        )

