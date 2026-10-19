# Guia de execução, demonstração e validação — PI II

**Requisitos:** Python 3.10+; conexão de internet na instalação de dependências; VS Code opcional; Windows PowerShell.

## Instalação passo a passo

```powershell
py --version
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py popular_demo
python manage.py runserver
```

Se o PowerShell bloquear a ativação, use o executável direto: `.venv\Scripts\python.exe manage.py migrate`, `.venv\Scripts\python.exe manage.py runserver` (e igualmente para os outros comandos). Acesse `http://127.0.0.1:8000/login/`.

## Roteiro para apresentação (10 minutos)
1. Faça login com conta criada localmente.
2. Abra Clientes e cadastre um cliente de demonstração.
3. Abra Produtos e cadastre um item com estoque, por exemplo R$ 18,50 e 8 unidades.
4. Abra Pedidos; adicione 2 unidades; finalize e confirme redução do estoque para 6.
5. Altere o status para Entregue e veja Relatórios e Painel.
6. Apresente a resposta de `/api/resumo/` enquanto autenticado.
7. Explique o modelo de dados (Cliente → Pedido → ItemPedido → Produto).
8. Execute `python manage.py test` e registre o resultado no relatório antes de afirmar sucesso.

## Testes e evidências
- `python scripts/auditar_codigo.py` verifica a estrutura e sintaxe Python, sem instalar Django.
- `python manage.py test` executa os testes integrados após instalar Django.
- `python manage.py check` faz as verificações internas do Django.
- `python manage.py makemigrations --check --dry-run` identifica mudanças não refletidas em migrações.
- Evidências de execução: capture prints do terminal e das telas reais (login, dashboard, pedidos, relatórios) e acrescente ao Word com legenda.

## API
`GET /api/resumo/` — requer login, JSON com números de clientes/produtos/pedidos.

## Importante
Projeto acadêmico local: DEBUG habilitado apenas no desenvolvimento, SQLite para demonstração e uso de dados fictícios. Não publicar as credenciais nem subir `db.sqlite3`. A implantação em nuvem não foi realizada nem validada neste pacote.
