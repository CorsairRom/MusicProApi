from datetime import datetime
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['codigo_pedido']
    
class PedidosViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()
    
class ResponseTransaction(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()
    
class ResponseIDView(APIView):
    def post(self, request):
        id = request.data.get('id')
        try:
            pedido = Pedido.objects.get(id=id)
            pedido.estado = True
            pedido.save()
            return Response({"message": "success", "data": pedido})
        except Pedido.DoesNotExist:
            return Response({"message": "error"})
    
# Host: https://webpay3g.transbank.cl
# Host: https://webpay3g.transbank.cl