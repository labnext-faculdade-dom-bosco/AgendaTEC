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

# Configuranco chave SSH
1. Abra o terminal e execute o comando:
    ```
    ssh-keygen -t rsa -b 4096 -C "seu_email@exemplo.com" -f ~/.ssh/id_azure_rsa
    ```
    Por padrão, as chaves serão salvas em:<br>
    ~/.ssh/id_rsa        (chave privada)<br>
    ~/.ssh/id_rsa.pub    (chave pública)<br>

    **OBS**: 
   - O parâmetro **-f** passa o caminho e nome do arquivo em que as chaves serão geradas. 
   Se não for passado, irá gerar um arquivo chamado id_rsa. Se você já tem uma chave SSH configurada 
   para seu email pessoal pode conflitar. Por isso, é recomendado utilizar um nome específico para diferenciá-la.


2. Inicie o agente SSH

    Windows (Git Bash):
    ```
    eval $(ssh-agent -s)
    ```
    Linux:
    ```
    eval "$(ssh-agent -s)"
    ```
    Adicione a chave:
    ```
    ssh-add ~/.ssh/id_azure_rsa
    ```
    Se a chave tiver uma passphrase, você vai precisar digitá-la aqui.


3. (opcional) Se você já possui uma chave SSH pessoal e não quer ter que informar qual chave 
utilizar para cada projeto, pode configurar a identificação automática para cada repositório.
    Para fazer isso, abra um arquivo com o comando:
    ```
    nano ~/.ssh/config 
    ```
    E preencha com os valores:
    ```
    Host github.com
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_rsa
       IdentitiesOnly yes

    Host ssh.dev.azure.com
       HostName ssh.dev.azure.com
       User git
       IdentityFile ~/.ssh/id_azure_rsa
       IdentitiesOnly yes
    ```
   **OBS:** No exemplo acima, a chave pessoal (Github) está no arquivo **id_rsa**, 
    e a chave do ambiente Labnext (Azure) está no arquivo **id_azure_rsa**. 
    Dessa forma, o git identifica qual chave usar de acordo com a origem do repositório, não sendo necessário informar
    qual chave deve ser utilizada em cada projeto.


4. Abra o arquivo da chave pública que você gerou e copie o texto dela (será utilizado nos passos seguintes).
    ```
    cat ~/.ssh/id_azure_rsa.pub
    ```
5. Acessar o Azure com o email institucional
6. Clique no ícone da engrenagem/configurações (User settings)
7. Clique na opção "SSH public keys"
8. Clique no sinal de adição (+ New Key)
9. Atribua um nome para a chave. Ex.: **<azure-ssh-key-seu-nome>**
10. Cole o texto que você copiou no passo 4 no campo "Public Key Data"

**OBS:** Nunca compartilhe a chave privada! Apenas a chave pública deve ir para o Azure.

# Clonando o repositório
Escolha uma pasta para organizar o projeto, e clone o repositório com o comando:
```
git clone https://labnextfdb@dev.azure.com/labnextfdb/AgendaTEC/_git/AgendaTEC
```

# Executando o projeto

### Configurar variáveis de ambiente
Em ambiente Windows:
```
copy .env.example .env
```

Em ambiente Linux:
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


### Realizando testes
#### 1. Executando teste específico:

```
docker compose exec web python3 manage.py test message.tests.WahaServiceTestCase.test_send_message
```

#### 2. Executando todos os testes da classe
```
docker compose exec web python3 manage.py test message.tests.WahaServiceTestCase
```

#### 3. Executando todos os testes do app
```
docker compose exec web python3 manage.py test message
```
Obs: 
- Substituir de acordo com o nome do app/classe/método. Nesse exemplo, os testes serão realizados no app **message**
que é utilizado para enviar mensagens pelo WhatsApp.

### Rotas

http://localhost:8000/ → Página principal da aplicação, onde ficam as views públicas do projeto. <br>
http://localhost:8000/admin/ → Painel administrativo do Django, gerenciado pelo Django Admin. 
Permite criar, editar e excluir registros do banco de dados.
