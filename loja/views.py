import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Cliente,Produto,Pedido,ItemPedido
from .forms import ClienteForm,ProdutoForm
class EntrarView(LoginView):
 template_name='loja/login.html'
@login_required
def dashboard(request):
 pedidos=list(Pedido.objects.select_related('cliente').prefetch_related('itens').order_by('-criado_em'))
 hoje=timezone.localdate()
 do_dia=[p for p in pedidos if timezone.localtime(p.criado_em).date()==hoje]
 vendas=sum((p.total for p in do_dia if p.status=='entregue'),Decimal('0'))
 return render(request,'loja/dashboard.html',{'pedidos':pedidos[:10],'pedidos_hoje':len(do_dia),'vendas':vendas,'clientes':Cliente.objects.count(),'produtos':Produto.objects.count()})
@login_required
def clientes(request):
 form=ClienteForm(request.POST or None)
 if request.method=='POST' and form.is_valid():form.save();return redirect('clientes')
 return render(request,'loja/cadastro.html',{'titulo':'Clientes','form':form,'registros':Cliente.objects.all(),'tipo':'cliente'})
@login_required
def produtos(request):
 form=ProdutoForm(request.POST or None)
 if request.method=='POST' and form.is_valid():form.save();return redirect('produtos')
 return render(request,'loja/cadastro.html',{'titulo':'Produtos','form':form,'registros':Produto.objects.all(),'tipo':'produto'})
@login_required
def pedidos(request):
 return render(request,'loja/pedidos.html',{'pedidos':Pedido.objects.select_related('cliente').prefetch_related('itens').order_by('-criado_em'),'clientes':Cliente.objects.all(),'produtos':Produto.objects.filter(estoque__gt=0)})
@login_required
@require_POST
def criar_pedido(request):
 try:
  payload=json.loads(request.body)
  cliente_id=int(payload['cliente']); itens=payload['itens']
  if not isinstance(itens,list) or not itens:raise ValueError('Adicione produtos ao pedido.')
  quantidades={}
  for item in itens:
   pid=int(item['produto']);qtd=int(item['quantidade'])
   if qtd<1:raise ValueError('Quantidade inválida.')
   quantidades[pid]=quantidades.get(pid,0)+qtd
  with transaction.atomic():
   cliente=Cliente.objects.get(pk=cliente_id)
   produtos={p.pk:p for p in Produto.objects.select_for_update().filter(pk__in=quantidades)}
   if len(produtos)!=len(quantidades):raise ValueError('Produto não encontrado.')
   for pid,qtd in quantidades.items():
    if produtos[pid].estoque<qtd:raise ValueError('Estoque insuficiente: '+produtos[pid].nome)
   pedido=Pedido.objects.create(cliente=cliente)
   for pid,qtd in quantidades.items():
    p=produtos[pid];ItemPedido.objects.create(pedido=pedido,produto=p,quantidade=qtd,preco_unitario=p.preco)
    p.estoque-=qtd;p.save(update_fields=['estoque'])
  return JsonResponse({'ok':True,'id':pedido.id})
 except (ValueError,TypeError,KeyError,Cliente.DoesNotExist,json.JSONDecodeError) as exc:
  return JsonResponse({'ok':False,'erro':str(exc)},status=400)
@login_required
@require_POST
def alterar_status(request,pk):
 status=request.POST.get('status')
 if status not in dict(Pedido.STATUS):return JsonResponse({'erro':'Status inválido'},status=400)
 with transaction.atomic():
  pedido=get_object_or_404(Pedido.objects.select_for_update(),pk=pk)
  if pedido.status=='cancelado' and status!='cancelado':return JsonResponse({'erro':'Pedido cancelado não pode ser reaberto'},status=400)
  if pedido.status=='entregue' and status=='cancelado':return JsonResponse({'erro':'Pedido entregue não pode ser cancelado'},status=400)
  if status=='cancelado' and pedido.status!='cancelado':
   for item in pedido.itens.all():
    p=Produto.objects.select_for_update().get(pk=item.produto_id)
    p.estoque+=item.quantidade;p.save(update_fields=['estoque'])
  pedido.status=status;pedido.save(update_fields=['status'])
 return redirect('pedidos')
@login_required
def relatorios(request):
 entregues=list(Pedido.objects.filter(status='entregue').select_related('cliente').prefetch_related('itens'))
 return render(request,'loja/relatorios.html',{'pedidos':entregues,'quantidade':len(entregues),'total':sum((p.total for p in entregues),Decimal('0'))})
@login_required
def api_resumo(request):
 return JsonResponse({'clientes':Cliente.objects.count(),'produtos':Produto.objects.count(),'pedidos':Pedido.objects.count()})
@require_POST
def sair(request):logout(request);return redirect('login')
