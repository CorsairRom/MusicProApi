from rest_framework import serializers

from api.models import Producto, DetallePedido, Pedido, Usuario


class SerializadorUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'is_staff': instance.is_staff,
            'is_superuser': instance.is_superuser
        }
        return data

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

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


    
    
    
    