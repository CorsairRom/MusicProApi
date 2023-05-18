from datetime import datetime
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from api.serializer import ProductoSerializer, DetallePedidoSerializer,PedidoSerializer
from api.models import Producto, DetallePedido, Pedido

# Create your views here.
class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
    
class ProductoWithStockViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.exclude(stock_pro = 0)
    
class DetallePedidorViewSet(viewsets.ModelViewSet):
    serializer_class = DetallePedidoSerializer
    queryset = DetallePedido.objects.all()
    
class PedidosViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()