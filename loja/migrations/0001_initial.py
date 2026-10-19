# Migração inicial do Projeto Integrador II.
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Cliente', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('nome',models.CharField(max_length=120)),
            ('email',models.EmailField(blank=True,max_length=254)),
            ('telefone',models.CharField(blank=True,max_length=25)),
        ]),
        migrations.CreateModel(name='Produto', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('nome',models.CharField(max_length=120)),
            ('preco',models.DecimalField(decimal_places=2,max_digits=10)),
            ('estoque',models.PositiveIntegerField(default=0)),
        ]),
        migrations.CreateModel(name='Pedido', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('criado_em',models.DateTimeField(auto_now_add=True)),
            ('status',models.CharField(choices=[('pendente','Pendente'),('preparo','Em preparo'),('entregue','Entregue'),('cancelado','Cancelado')],default='pendente',max_length=12)),
            ('cliente',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to='loja.cliente')),
        ]),
        migrations.CreateModel(name='ItemPedido', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('quantidade',models.PositiveIntegerField()),
            ('preco_unitario',models.DecimalField(decimal_places=2,max_digits=10)),
            ('pedido',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='itens',to='loja.pedido')),
            ('produto',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to='loja.produto')),
        ]),
    ]
