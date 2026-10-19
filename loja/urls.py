from django.urls import path
from . import views
urlpatterns=[path('login/',views.EntrarView.as_view(),name='login'),path('sair/',views.sair,name='sair'),path('',views.dashboard,name='dashboard'),path('clientes/',views.clientes,name='clientes'),path('produtos/',views.produtos,name='produtos'),path('pedidos/',views.pedidos,name='pedidos'),path('pedidos/criar/',views.criar_pedido,name='criar_pedido'),path('pedidos/<int:pk>/status/',views.alterar_status,name='alterar_status'),path('relatorios/',views.relatorios,name='relatorios'),path('api/resumo/',views.api_resumo,name='api_resumo')]
