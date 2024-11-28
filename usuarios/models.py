from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = (
    ('administrador', 'Administrador'),
    ('editor', 'Editor'),
    ('usuario', 'Usuario'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)#Relación uno a uno con la tabla User
    rol=models.CharField(max_length=20,choices=ROLES,default='usuario')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"