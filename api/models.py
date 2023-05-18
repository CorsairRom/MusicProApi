from django.db import models

# Create your models here.


class Producto(models.Model):
    nom_pro = models.CharField(max_length=50)
    desc_pro = models.CharField(max_length=250)
    cat_pro = models.CharField(max_length=100)
    precio_pro = models.PositiveIntegerField()
    stock_pro = models.IntegerField()
    
    def __str__(self):
        return self.nom_pro
 
class DetallePedido(models.Model):
    codigo_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cant_producto= models.PositiveIntegerField() 
    subtotal = models.PositiveIntegerField( default=0)
    
    def save(self, *args, **kwargs):
        producto = self.codigo_producto
        precio_producto = producto.precio_pro
        subtotal = precio_producto * self.cant_producto
        self.subtotal = subtotal
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.codigo_producto)
    
    
class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    rut_cliente = models.CharField(max_length=12)
    codigo_sucursal = models.IntegerField()
    detalle_pedido = models.ForeignKey(DetallePedido, on_delete=models.CASCADE, default=1)
    
    
    def __str__(self):
        return str(self.id)
    
