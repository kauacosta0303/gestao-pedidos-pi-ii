from decimal import Decimal
from django.db import models
class Cliente(models.Model):
 nome=models.CharField(max_length=120)
 email=models.EmailField(blank=True)
 telefone=models.CharField(max_length=25,blank=True)
 def __str__(self):return self.nome
class Produto(models.Model):
 nome=models.CharField(max_length=120)
 preco=models.DecimalField(max_digits=10,decimal_places=2)
 estoque=models.PositiveIntegerField(default=0)
 def __str__(self):return self.nome
class Pedido(models.Model):
 STATUS=[('pendente','Pendente'),('preparo','Em preparo'),('entregue','Entregue'),('cancelado','Cancelado')]
 cliente=models.ForeignKey(Cliente,on_delete=models.PROTECT)
 criado_em=models.DateTimeField(auto_now_add=True)
 status=models.CharField(max_length=12,choices=STATUS,default='pendente')
 @property
 def total(self):return sum((i.subtotal for i in self.itens.all()),Decimal('0'))
 def __str__(self):return f'Pedido #{self.pk}'
class ItemPedido(models.Model):
 pedido=models.ForeignKey(Pedido,on_delete=models.CASCADE,related_name='itens')
 produto=models.ForeignKey(Produto,on_delete=models.PROTECT)
 quantidade=models.PositiveIntegerField()
 preco_unitario=models.DecimalField(max_digits=10,decimal_places=2)
 @property
 def subtotal(self):return self.quantidade*self.preco_unitario
