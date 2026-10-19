import json
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Cliente, Produto, Pedido, ItemPedido

class SistemaTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('teste', password='SenhaSegura123!')
        self.cliente = Cliente.objects.create(nome='Maria Silva')
        self.produto = Produto.objects.create(nome='Café', preco=Decimal('15.50'), estoque=10)

    def entrar(self):
        self.client.force_login(self.usuario)

    def test_autenticacao_obrigatoria(self):
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 302)
        self.assertEqual(self.client.get(reverse('api_resumo')).status_code, 302)

    def test_cadastro_produto_autenticado(self):
        self.entrar()
        resposta = self.client.post(reverse('produtos'), {'nome':'Água','preco':'3.50','estoque':'12'})
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Produto.objects.filter(nome='Água').exists())

    def test_total_usa_preco_do_momento_da_venda(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        ItemPedido.objects.create(pedido=pedido, produto=self.produto, quantidade=2, preco_unitario=Decimal('15.50'))
        self.assertEqual(pedido.total, Decimal('31.00'))

    def test_api_resumo(self):
        self.entrar()
        self.assertEqual(self.client.get(reverse('api_resumo')).json()['produtos'], 1)

    def test_pedido_baixa_estoque(self):
        self.entrar()
        resposta = self.client.post(reverse('criar_pedido'), data=json.dumps({'cliente':self.cliente.id,'itens':[{'produto':self.produto.id,'quantidade':3}]}), content_type='application/json')
        self.assertEqual(resposta.status_code,200)
        self.assertTrue(resposta.json()['ok'])
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque,7)

    def test_sem_estoque_nao_cria_pedido(self):
        self.entrar()
        resposta = self.client.post(reverse('criar_pedido'), data=json.dumps({'cliente':self.cliente.id,'itens':[{'produto':self.produto.id,'quantidade':99}]}), content_type='application/json')
        self.assertEqual(resposta.status_code,400)
        self.assertEqual(Pedido.objects.count(),0)

    def test_cancelamento_devolve_estoque(self):
        self.entrar()
        resposta=self.client.post(reverse('criar_pedido'),data=json.dumps({'cliente':self.cliente.id,'itens':[{'produto':self.produto.id,'quantidade':2}]}),content_type='application/json')
        pedido_id=resposta.json()['id']
        self.client.post(reverse('alterar_status',args=[pedido_id]),{'status':'cancelado'})
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque,10)
