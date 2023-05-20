from rest_framework import serializers

from api.models import Producto, DetallePedido, Pedido

class ProductoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Producto
        fields = '__all__'
        
class DetallePedidoSerializer(serializers.ModelSerializer):
    
    codigo_producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='codigo_producto',
        write_only=True,
    )
    codigo_producto = serializers.SerializerMethodField()
    
    class Meta:
        model = DetallePedido
        fields = '__all__'
        
    def get_codigo_producto(self, obj):
        return {'id': obj.codigo_producto.id, 'nombre': obj.codigo_producto.nom_pro}    

class PedidoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pedido
        fields = '__all__'


    
    
    
    