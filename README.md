# Catálogo de Amostras — LTPOA

Esboço inicial de um sistema responsivo para cadastrar e acompanhar amostras de mel, leite e outros produtos no laboratório LTPOA.

## Recursos disponíveis

- Solicitação de conta com aprovação por administrador
- Login e logout
- Painel com resumo dos status
- Cadastro, consulta, busca, filtros e edição de amostras
- Administração de usuários e amostras em `/admin/`
- Interface responsiva para celular e computador
- Configuração pronta para Django, PostgreSQL e Render

## Executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/`. Para aprovar uma conta solicitada, abra `/admin/`, entre como superusuário e marque o usuário como ativo.

## Implantar no Render

Envie o projeto para um repositório Git e, no painel do Render, crie um Blueprint usando o arquivo `render.yaml`. Depois da primeira implantação, abra o Shell do serviço e execute `python manage.py createsuperuser`.

Não armazene anexos no disco local do serviço. Quando fotos ou laudos forem adicionados ao sistema, configure um serviço de armazenamento de objetos.
