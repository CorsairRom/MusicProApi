from rest_framework.routers import DefaultRouter
from api.views import ProductoViewSet,ProductoWithStockViewSet,PedidosViewSet,DetallePedidorViewSet, ResponseIDView
from django.urls import path
router = DefaultRouter()

router.register(r'producto', ProductoViewSet, basename="producto")
router.register(r'producto-stock', ProductoWithStockViewSet, basename="productoStock")
router.register(r'detalle', DetallePedidorViewSet, basename="detalle")
router.register(r'pedido', PedidosViewSet, basename="pedido")



urlpatterns = router.urls + [
    path('responseid/', ResponseIDView.as_view(), name='response-id'),
]