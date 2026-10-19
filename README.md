# Sistema Web de Gestão de Pedidos — Projeto Integrador II (UNIVESP)

**Orientador:** Kennedy Ronald Cárdenas Fuentes Rivera  
**Equipe:** Kauã Gabriel da Costa (23202622); Vinícius Roque Paes de Almeida (24208304); Kauã Soares dos Santos (24203174).

## Arquitetura
Frontend HTML + CSS + JavaScript → aplicação Django (Python, autenticação, regras, API) → SQLite (desenvolvimento local).

## Funcionalidades implementadas no código
- Login/logout com autenticação Django;
- Cadastro de clientes e produtos;
- Criação de pedidos com múltiplos itens, baixa de estoque e validação;
- Atualização de status e cancelamento com devolução do estoque;
- Dashboard, relatório simples e API de resumo autenticada;
- Migração inicial, comando de dados fictícios e testes automatizados.

## Rodar no Windows
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py popular_demo
python manage.py runserver
```
Depois acesse http://127.0.0.1:8000/login/ e use o usuário criado.

## Verificar
```powershell
python scripts/auditar_codigo.py
python manage.py check
python manage.py test
```
O primeiro comando é estático (não precisa de Django). Os outros requerem dependências instaladas. Consulte o roteiro completo em `docs/GUIA_EXECUCAO_E_TESTES.md`.

## GitHub
```bash
git init
git add .
git commit -m "Entrega acadêmica do PI II"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/gestao-pedidos-pi-ii.git
git push -u origin main
```

## Estado real do projeto
A estrutura e sintaxe Python foram auditadas; testes de execução Django precisam ser feitos após instalar as dependências no computador da equipe. **Nuvem, pesquisa presencial e validação com comerciantes não foram comprovadas neste material**; não confundir diagramas e telas ilustrativas com prints de aplicação real. Este código **não é para produção pública** sem endurecimento de segurança, revisão de CSRF/autorização, HTTPS, coleta de logs, backup e configurações apropriadas.
