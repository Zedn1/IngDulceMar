from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('ingresosygastos/', views.ingresos_y_gastos, name='ingresos_y_gastos'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos-proveedores/', views.pedidos_proveedores, name='pedidos_proveedores'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('<int:id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('<int:id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),
    path('eliminar_producto/<int:detalle_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto1, name='eliminar_producto1'),
    path('productos/actualizar-stock/<int:pk>/', views.actualizar_stock, name='actualizar_stock'),

]