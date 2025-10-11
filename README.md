# Estrutura do projeto
```plaintext
AgendaTEC/

├── .env                 # Variáveis de ambiente (Esse arquivo nunca é enviado para o repositório!)
├── .env.example         # Exemplo das variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo git
├── Dockerfile           # Criação da imagem do container da aplicação
├── docker compose.yml   # Orquestração dos containers
├── manage.py            # Utilizado para interagir com o projeto via linha de comando
├── requirements.txt     # Dependências do projeto
│
├── core/                # Diretório com as configurações globais do projeto
│   ├── __init__.py      # Torna o diretório um pacote Python
│   ├── settings.py      # Configurações gerais do projeto (DB, apps, middlewares etc.)
│   ├── urls.py          # Arquivo principal de rotas/URLs do projeto
│   ├── asgi.py          # Configuração para servidores ASGI (WebSockets, etc.)
│   └── wsgi.py          # Configuração para servidores WSGI (produção tradicional)
│
└── app/
    ├── __init__.py             
    ├── admin.py         # Registro dos modelos para o admin do Django
    ├── apps.py          # Configuração do app para o Django
    ├── models.py        # Definição das classes que representam as tabelas do banco de dados
    ├── views.py         # Funções ou classes que retornam respostas (lógica de exibição)
    ├── urls.py          # (opcional) Rotas específicas do app
    ├── forms.py         # (opcional) Formulários baseados em Django Forms ou ModelForms
    ├── tests.py         # (opcional) Testes automatizados (usando unittest ou pytest)
    └── migrations/      # Histórico de migrações do banco de dados
        └── __init__.py
```

# Iniciando

## Pré-requisitos

#### Obrigatórios:
- [Python 3.10+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

#### Opcionais:
- [PyCharm](https://www.jetbrains.com/pycharm/)

**Observações:** 
- O PyCharm, assim como outras IDEs da [JetBrains](https://www.jetbrains.com/) 
pode ser utilizado na versão Professional de forma gratuita com o email institucional. 

# Executando o projeto

### Configurar variáveis de ambiente
```
cp .env.example .env
```
Em seguida, altere os valores conforme necessário.


### Criar containers e subir a aplicação
Realiza o build da aplicação, utilizado na primeira execução ou quando a estrutura do projeto é alterada.
Ex.: Adição de novas bibliotecas, imagens, etc.
```
docker compose up --build -d
```

Sobe a aplicação sem realizar o build.
```
docker compose up
```

Derruba os containers e para a aplicação
```
docker compose down
```

### Banco de dados
Para interagir com o banco de dados utilizamos o conceito de `migrações`.

O comando de criar migrações percorre todo o projeto e verifica se algum modelo foi criado ou alterado, 
O comando seguinte aplica de fato essas alterações no banco de dados, criando e/ou alterando tabelas.

1. Criar migrações
```
docker compose exec web python3 manage.py makemigrations
```

2. Aplicar migrações
```
docker compose exec web python3 manage.py migrate
```

3. Criar superusuário (opcional)
```
docker compose exec web python3 manage.py createsuperuser
```

**Observações:** 
- Na primeira vez executando o projeto, é necessário realizar os três passos acima.


### Criando novo app
No Django, um app é uma unidade modular de código que implementa uma funcionalidade específica do projeto.
```
docker compose exec web python3 manage.py startapp my_app_name
```
**Observações:** 
- Ao criar um novo `app` é necessário adicioná-lo em `INSTALLED_APPS` do arquivo `setting.py` 
para que o Django instale ele. 
- Em seguida, é necessário utilizar os comandos `makemigrations` e `migrate`, 
para criar as tabelas do novo `app` no banco de dados.


### Rotas

http://localhost:8000/ → Página principal da aplicação, onde ficam as views públicas do projeto. <br>
http://localhost:8000/admin/ → Painel administrativo do Django, gerenciado pelo Django Admin. 
Permite criar, editar e excluir registros do banco de dados.
