from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.sessions.models import Session

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from api.serializer import ProductoSerializer, DetallePedidoSerializer,PedidoSerializer, SerializadorUsuario
from api.models import Producto, DetallePedido, Pedido


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):

        login_serializer = self.serializer_class(
            data=request.data, context={'request': request})
        
        if not login_serializer.is_valid():
            return Response({'error': 'Usuario o contraseña incorrecta'},
                        status=status.HTTP_400_BAD_REQUEST)

        user = login_serializer.validated_data['user']
        if not user.is_active:
            return Response({'error': 'No se puede ingresar con usuario inactivo'},
                        status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = SerializadorUsuario(user)

        if not created:
            # Delete user token
            token.delete()
            # Delete all sessions for user
            all_sessions = Session.objects.filter(
                expire_date__gte=datetime.now())
            
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    # auth_user_id is the primary key's user on the session
                    if user.id == int(session_data.get('_auth_user_id')):
                        session.delete()

            return Response({'error': 'Su sessión quedo activa desde la última vez. Por favor ingrese nuevamente.'},
                            status=status.HTTP_400_BAD_REQUEST
                            )
    
        return Response({
                    'token': token.key,
                    'usuario': user_serializer.data,
                    'message': 'Ingreso exitoso.'
                }, status=status.HTTP_201_CREATED)

class Logout(APIView):
    def post(self, request, *args, **kwargs):
        try:
            token_request = request.GET.get('token')
            token = Token.objects.filter(key=token_request).first()

            if not token:
                return Response({'error': 'No hay usuario con ese token'},
                            status=status.HTTP_400_BAD_REQUEST)
            
            user = token.user

            token.delete()
            # Delete all sessions for user
            all_sessions = Session.objects.filter(
                expire_date__gte=datetime.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    # auth_user_id is the primary key's user on the session
                    if user.id == int(session_data.get('_auth_user_id')):
                        session.delete()

            token_message = 'Token eliminado.'
            session_message = 'Sesión exitosamente cerrada.'

            return Response({'token_message': token_message,
                            'session_message': session_message},
                            status=status.HTTP_200_OK)

        except:
            return Response({'error': 'No se ha encontrado el token ingresado'},
                            status=status.HTTP_409_CONFLICT)
        
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
    
    def create(self, request, *args, **kwargs):
        
        producto_id = request.data.get('codigo_producto_id')
        cantidad = int(request.data.get('cant_producto'))
        
        try:
            producto = Producto.objects.get(pk= producto_id)
            
            if producto.stock_pro < cantidad:
                return Response({
                    "Error": "No Hay suficiente stock", "cod": "400"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            producto.save()
            
            return super().create(request, *args, **kwargs)
        except Producto.DoesNotExist:
            return Response(
                {'error': 'El producto especificado no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
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