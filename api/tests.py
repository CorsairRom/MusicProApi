from django.test import TestCase, Client
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from .models import Producto, Pedido


#probar todos los crud
class test_response_status_producto(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tes = Client()
        
    def test_get_producto(self):
        url = '/api/producto/'
        response = self.client.get(url)
        print( 'Test Status conexion endpoint producto')
        esperado = status.HTTP_200_OK
        conseguido = response.status_code
        print('Respuesta esperada: ', esperado)
        self.assertEqual(conseguido, esperado, msg={'MSG': "Lista de productos"})
        print('Respuesta Conseguida: ', conseguido)
        if esperado == conseguido:
            print('Test Ok!')
        else:
            print('Fail!')

        self.assertEqual(len(response.data), Producto.objects.count())
    
    
        
        
    
  
class AddProductos(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tes = Client()
        self.producto = {
          'nom_pro' : 'Guitarra Electrica Gibsson',
          'desc_pro' : 'Una esclusiva guitarra electrica para entusiastas',
          'cat_pro' : "Guitarras electricas",
          'precio_pro' : 60000,
          'stock_pro' : 4
        }
        # self.producto_created = Producto.objects.create(**producto)
        
    def test_post_producto(self):
        print('Test Producto')
        url = '/api/producto/'
        response = self.client.get(url)
        producto_created = self.client.post(url, self.producto)
        
        #comprobar si fue creado
        self.assertEqual(producto_created.status_code, 201, 'Producto not created')
        
        #comprobar la cantidad de producto agregado solo sea 1
        cant_productos = Producto.objects.count()
        self.assertEqual(1, 1, 'Not equal')
        if cant_productos == 1:
            print('sucess!')
            

class AddPedido(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tes = Client()
        self.pedido = {
           'rut_cliente' : '18.202.300-0',
            'codigo_sucursal' : '1',
        }
        # Pedido.objects.create(**pedido)
        
    def test_post_pedido(self):
        print('test pedido')
        url = '/api/pedido/'
        response = self.client.get(url)
        pedido_created = self.client.post(url, self.pedido)
        
        #comprobar si fue creado
        self.assertEqual(pedido_created.status_code, 201, 'Pedido not created')

        #Imprimir la data creada
        if pedido_created.status_code == 201:
            print('Sucess!')
            print(pedido_created.content)
            
class AddDetalle(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tes = Client()
        self.addProductos = AddProductos()
        self.addpedido = AddPedido()
        AddPedido
        self.detalle = {
        'codigo_producto_id' : 1,
        'codigo_pedido' : 1,
        'cant_producto' : 2
        }
    
    def test_post_detalle(self):
        print('Test Detalle pedido')
        url = '/api/detalle/'
        response = self.client.get(url)
        self.addProductos.setUp()
        self.addpedido.setUp()
        self.addProductos.test_post_producto()
        self.addpedido.test_post_pedido()
        productos = Producto.objects.get(pk=1)
        pedido = Pedido.objects.get(pk=1).id
        detalle_created = self.client.post(url, self.detalle)
        
        self.assertEqual(detalle_created.status_code, 201)
        print("Producto", productos)
        print("pedido",pedido)
            