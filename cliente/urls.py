from django.urls import path
from . import views
from .views import *

app_name = 'cliente'

urlpatterns = [
    path('', ClienteListView.as_view(), name="cliente-list"),
    path('nuevo', ClienteCreateView.as_view(), name="cliente-nuevo"),
    path('cliente/<int:pk>/editar/', ClienteUpdateView.as_view(), name="cliente-editar"),
    path('cliente/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detalle'),
    path('cliente/<int:cliente_id>/beneficiario/crear/',views.crear_beneficiario,name='beneficiario-crear'),
    path('beneficiario/<int:beneficiario_id>/eliminar/',views.eliminar_beneficiario,name='beneficiario-eliminar'),
]
