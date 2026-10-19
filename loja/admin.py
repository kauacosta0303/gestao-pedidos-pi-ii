from django.contrib import admin
from .models import Cliente,Produto,Pedido,ItemPedido
admin.site.register([Cliente,Produto,Pedido,ItemPedido])
