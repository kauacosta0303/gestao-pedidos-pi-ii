from django import forms
from .models import Cliente,Produto
class ClienteForm(forms.ModelForm):
 class Meta:
  model=Cliente
  fields=['nome','email','telefone']
class ProdutoForm(forms.ModelForm):
 class Meta:
  model=Produto
  fields=['nome','preco','estoque']
