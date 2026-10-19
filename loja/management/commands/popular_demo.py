from decimal import Decimal
from django.core.management.base import BaseCommand
from loja.models import Cliente, Produto, Pedido, ItemPedido

class Command(BaseCommand):
    help = 'Cria dados fictícios e seguros para a apresentação acadêmica.'
    def handle(self, *args, **options):
        clientes = [
            Cliente.objects.get_or_create(nome='Ana Ribeiro',defaults={'email':'ana@example.org'})[0],
            Cliente.objects.get_or_create(nome='Carlos Lima',defaults={'email':'carlos@example.org'})[0],
        ]
        produtos = [
            Produto.objects.get_or_create(nome='Café moído 500 g',defaults={'preco':Decimal('24.90'),'estoque':30})[0],
            Produto.objects.get_or_create(nome='Pão de forma',defaults={'preco':Decimal('12.50'),'estoque':20})[0],
            Produto.objects.get_or_create(nome='Suco integral 1 L',defaults={'preco':Decimal('15.00'),'estoque':15})[0],
        ]
        if not Pedido.objects.exists():
            pedido = Pedido.objects.create(cliente=clientes[0],status='entregue')
            ItemPedido.objects.create(pedido=pedido,produto=produtos[0],quantidade=2,preco_unitario=produtos[0].preco)
            produtos[0].estoque -= 2
            produtos[0].save(update_fields=['estoque'])
            self.stdout.write('Pedido demonstrativo #'+str(pedido.pk)+' criado com baixa de estoque.')
        self.stdout.write(self.style.SUCCESS('Dados demonstrativos preparados.'))
