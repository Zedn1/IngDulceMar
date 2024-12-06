from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('ingresosygastos/', views.ingresos_y_gastos, name='ingresos_y_gastos'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos-proveedores/', views.pedidos_proveedores, name='pedidos_proveedores'),
]