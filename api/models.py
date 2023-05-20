from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import F
# Create your models here.


class Producto(models.Model):
    nom_pro = models.CharField(max_length=50)
    desc_pro = models.CharField(max_length=250)
    cat_pro = models.CharField(max_length=100)
    precio_pro = models.PositiveIntegerField()
    stock_pro = models.PositiveIntegerField()
    
    def save(self, *args, **kwargs):
        if self.stock_pro < 0:
            raise ValidationError("El stock no puede ser menor a 0")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nom_pro
  
class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    rut_cliente = models.CharField(max_length=12)
    codigo_sucursal = models.IntegerField()
    total = models.PositiveIntegerField(null=True, blank=True)
    estado = models.BooleanField(default=False)    
    
    def __str__(self):
        return str(self.id)
    
class DetallePedido(models.Model):
    codigo_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    codigo_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, default=1)
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
    

 
@receiver(post_save, sender= DetallePedido)
def actualizar_stock(sender, instance, **kwargs):
    if kwargs.get('created', False):
        producto = instance.codigo_producto
        producto.stock_pro -= instance.cant_producto
        producto.save()
   
@receiver(post_save, sender=Producto)
def actualizar_detalles(sender, instance, **kwargs):
    DetallePedido.objects.filter(codigo_producto=instance).update(subtotal=instance.precio_pro* F('cant_producto'))
