"""Verificação ESTÁTICA sem Django: existência de arquivos e sintaxe Python."""
from pathlib import Path
import ast
base=Path(__file__).resolve().parents[1]
obrigatorios=['manage.py','config/settings.py','loja/models.py','loja/views.py','loja/urls.py','loja/tests.py','loja/migrations/0001_initial.py','static/js/pedidos.js','static/css/style.css','templates/loja/dashboard.html','templates/loja/pedidos.html']
faltantes=[f for f in obrigatorios if not (base/f).is_file()]
arquivos=list(base.rglob('*.py'))
erros=[]
for a in arquivos:
    try:ast.parse(a.read_text(encoding='utf-8'),filename=str(a))
    except SyntaxError as e:erros.append(f'{a}: {e}')
print(f'Arquivos obrigatórios: {len(obrigatorios)-len(faltantes)}/{len(obrigatorios)}')
print(f'Arquivos Python analisados: {len(arquivos)}')
print(f'Erros de sintaxe Python: {len(erros)}')
if faltantes or erros:
    print('Faltam:',faltantes,'Erros:',erros)
    raise SystemExit(1)
print('Auditoria ESTÁTICA aprovada. Não substitui os testes Django.')
