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


# Configuração de chave SSH e clone do repositório

Para clonar um repositório do GitHub via SSH, cada pessoa precisa ter um par de chaves (uma privada e uma pública) e cadastrar a chave pública na própria conta do GitHub. Isso evita digitar usuário e senha toda vez que for usar o Git.

Siga os passos na ordem, usando o Git Bash (recomendado no Windows) ou o terminal do seu sistema operacional.

## Pré-requisitos

- Git instalado na máquina (o Git Bash já vem junto no Windows)
- Conta pessoal no [GitHub](https://github.com)
- Acesso liberado como colaborador no repositório `labnext-faculdade-dom-bosco/AgendaTEC`

## Passo 1: Verificar se já existe uma chave SSH

```bash
ls -al ~/.ssh
```

Esse comando lista os arquivos da pasta `.ssh`. Se já existirem os arquivos `id_ed25519` e `id_ed25519.pub`, pule direto para o Passo 5. Se a pasta não existir ou esses arquivos não aparecerem, siga para o próximo passo.

Se o comando acima retornar um erro como `No such file or directory`, a pasta `.ssh` ainda não existe na sua máquina. Nesse caso, crie ela com:

```bash
mkdir ~/.ssh
```

## Passo 2: Gerar uma nova chave SSH

```bash
ssh-keygen -t ed25519 -C "seuemail@exemplo.com"
```

Troque `seuemail@exemplo.com` pelo e-mail cadastrado no seu GitHub. O `-t ed25519` define o tipo de chave (mais moderno e seguro que o antigo RSA) e o `-C` adiciona um comentário só para identificar a chave depois.

O terminal vai fazer duas perguntas:

- `Enter file in which to save the key`: aperte Enter para aceitar o local padrão.
- `Enter passphrase`: uma senha extra, opcional, para proteger a chave. Pode digitar uma senha ou deixar em branco (Enter duas vezes). Atenção: se escolher usar senha, digite exatamente igual nas duas vezes, senão aparece `Passphrases do not match` e o processo pede de novo.

Ao final, aparece uma mensagem parecida com esta, confirmando que a chave foi criada, incluindo o desenho (randomart) gerado a partir da chave:

```
Your identification has been saved in /c/Users/seu-usuario/.ssh/id_ed25519
Your public key has been saved in /c/Users/seu-usuario/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx seuemail@exemplo.com
The key's randomart image is:
+--[ED25519 256]--+
|      .oo.       |
|     o  ..o      |
|    . .  o .     |
|   .  oo+.o      |
|    ..o+S..      |
|   .  +.=.+      |
|    o..*.*.+     |
|   . +.=.O.o     |
|    .+=+E+o      |
+----[SHA256]-----+
```

O fingerprint e o desenho mudam a cada chave gerada, então o seu vai ser diferente do exemplo acima. O importante é essas linhas aparecerem, confirmando que a chave foi salva com sucesso.

## Passo 3: Configurar o ssh-agent como serviço do Windows

Isso só precisa ser feito uma vez em cada computador. Abra o PowerShell como Administrador (clique com o botão direito no ícone do PowerShell e escolha "Executar como administrador") e rode:

```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
```

Isso configura o ssh-agent para iniciar sozinho junto com o Windows, em vez de precisar ser iniciado manualmente a cada terminal novo.

## Passo 4: Adicionar a chave ao ssh-agent

De volta ao Git Bash, adicione a chave criada no Passo 2:

```bash
ssh-add ~/.ssh/id_ed25519
```

Como o ssh-agent agora roda como serviço do Windows, a chave fica guardada e carregada automaticamente mesmo depois de reiniciar o computador. Não deve ser necessário repetir esse comando depois disso.

## Passo 5: Copiar a chave pública

```bash
cat ~/.ssh/id_ed25519.pub
```

Isso mostra o conteúdo da chave pública no terminal. Copie tudo, do início (`ssh-ed25519`) até o final (o e-mail usado no `-C`).

Importante: nunca compartilhe o arquivo `id_ed25519` (sem o `.pub`). Ele é a chave privada e deve ficar só na sua máquina.

## Passo 6: Cadastrar a chave pública no GitHub

1. Entre no GitHub e clique na sua foto de perfil, no canto superior direito.
2. Vá em **Settings**.
3. No menu lateral esquerdo, clique em **SSH and GPG keys**.
4. Clique em **New SSH key**.
5. Em **Title**, coloque um nome que identifique o computador (por exemplo, "Notebook pessoal").
6. Em **Key**, cole a chave pública copiada no Passo 5.
7. Clique em **Add SSH key**. O GitHub pode pedir a senha da conta ou o código de autenticação de dois fatores para confirmar.

## Passo 7: Testar a conexão

```bash
ssh -T git@github.com
```

Na primeira conexão, pode aparecer uma pergunta perguntando se quer continuar: digite `yes` e aperte Enter. Se estiver tudo certo, a resposta será parecida com:

```
Hi seu-usuario! You've successfully authenticated, but GitHub does not provide shell access.
```

Essa mensagem confirma que a chave SSH está funcionando.

## Passo 8: Clonar o repositório

No mesmo terminal que você já vem usando (não precisa abrir o explorador de arquivos), use o `cd` para entrar na pasta onde quer guardar o projeto. O caminho `~/Documents` abaixo é só um exemplo, troque pelo caminho que você preferir:

```bash
cd ~/Documents
```

Depois, clone o repositório:

```bash
git clone git@github.com:labnext-faculdade-dom-bosco/AgendaTEC.git
```

Isso cria uma pasta chamada `AgendaTEC` com todo o código do projeto.

## Passo 9: Conferir se deu certo

```bash
cd AgendaTEC
git status
```

Se aparecer algo como `On branch develop, nothing to commit, working tree clean`, o clone funcionou.

# Executando o projeto
Com o projeto clonado abra na sua IDE e siga os passos abaixo:

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

**Observações:**
- Por padrão, `docker compose up` sobe **apenas** os containers `web` (Django) e `db` (Postgres), o suficiente pra desenvolver e testar a maior parte do projeto.
- Acesse a aplicação em **http://localhost:8000** (repare que é `http`, não `https`). Veja a seção "Arquivos docker-compose e ambientes" mais abaixo para entender por quê.
- `waha`, `redis`, `celery_worker` e `celery_beat` só existem pra funcionalidades que dependem de WhatsApp/tarefas agendadas, e ficam atrás do profile `prod`. Se precisar testar isso localmente, suba com:
```
docker compose --profile prod up -d
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


# Arquivos docker-compose e ambientes

O projeto usa três arquivos de compose, cada um com uma função específica.
Na maioria das vezes você não precisa escolher nenhum na mão: o Compose
decide sozinho com base no que está (ou não está) definido no `.env`.

| Arquivo | Quando é carregado | Para que serve |
|---|---|---|
| `docker-compose.yml` | sempre | Base do projeto: `web` e `db` sempre ativos. `waha`, `redis`, `celery_worker` e `celery_beat` também estão definidos aqui, mas atrás do profile `prod`. |
| `docker-compose.override.yml` | automático, sempre que o arquivo existir e `COMPOSE_FILE` não estiver definido no `.env` (ou seja, em dev) | Publica a porta `8000` pro host, só pra dar acesso direto ao Django pelo navegador em dev, sem precisar do Caddy. |
| `docker-compose.prod.yml` | só quando `COMPOSE_FILE` está definido explicitamente no `.env` | Liga `web` e `waha` na rede externa `caddy_net`, que é como o Caddy compartilhado (outro repositório, ver seção abaixo) alcança esses containers. |

## Desenvolvimento (padrão, sem mexer em nada)

```bash
docker compose up -d
```

Isso sobe só `web` e `db`. Acesse em:

```
http://localhost:8000
```

Repare que é `http`, não `https`: o `runserver` do Django só fala HTTP. Se o
navegador reescrever sozinho o endereço pra `https://localhost:8000` (alguns
navegadores têm um modo "só conexões seguras" que faz isso automaticamente),
o log do container `web` mostra um erro estranho, parecido com:

```
code 400, message Bad request version (...)
You're accessing the development server over HTTPS, but it only supports HTTP.
```

A correção é digitar o `http://` por completo na barra de endereços (ou
desativar esse modo do navegador para `localhost`), não é um problema de
configuração do projeto.

Se precisar testar localmente as funcionalidades que dependem de
WhatsApp/tarefas agendadas (`waha`, `redis`, `celery_worker`, `celery_beat`):

```bash
docker compose --profile prod up -d
```

**Atenção ao derrubar os containers:** o `docker compose down` precisa ser
chamado com o mesmo profile usado pra subir. Se você subiu com
`--profile prod` e depois roda só `docker compose down`, alguns containers
ficam órfãos presos na rede interna, e o Docker recusa remover essa rede
(erro do tipo `Network ... still in use`). Na dúvida, use sempre:

```bash
docker compose --profile prod down
```

## Produção: proxy reverso e HTTPS

O Caddy (proxy reverso + certificado HTTPS) **não faz parte deste
repositório**. Ele roda como um serviço compartilhado, no servidor, usado por
vários projetos ao mesmo tempo, no repositório
[`labnext-caddy`](https://github.com/labnext-faculdade-dom-bosco/labnext-caddy).

O que fica aqui, do lado do AgendaTEC:
- [`deploy/caddy/agendatec.caddy`](deploy/caddy/agendatec.caddy): as rotas do
  AgendaTEC para o Caddy compartilhado. É esse arquivo que muda se uma rota
  nova for adicionada (ex.: um novo endpoint de API).
- [`docker-compose.prod.yml`](docker-compose.prod.yml): liga `web` e `waha`
  na rede externa `caddy_net` (ver tabela no início desta seção).

No servidor, depois de criar a rede uma única vez:

```bash
docker network create caddy_net
```

adicione estas duas linhas no `.env` do servidor:

```env
COMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml
COMPOSE_PROFILES=prod
```

A partir daí, o comando de sempre já faz tudo sozinho, sem precisar lembrar
de `-f` nem `--profile` toda vez:

```bash
docker compose up -d
```

(Se preferir não mexer no `.env`, o mesmo resultado sai de
`docker compose -f docker-compose.yml -f docker-compose.prod.yml --profile prod up -d`.)

Nesse cenário, acesse em `https://teste.agendatec.faculdadedombosco.net.br`
(o domínio real do servidor), e não mais em `http://localhost:8000` (essa
porta nem fica publicada em produção, ver tabela no início desta seção).

## Testando o fluxo completo (AgendaTEC + Caddy) sem precisar de um servidor

Dá pra simular o ambiente de produção inteiro na sua própria máquina,
incluindo o Caddy, sem precisar de DNS real nem de certificado de verdade. O
passo a passo completo está no `README.md` do repositório `labnext-caddy`,
seção "Testando localmente". Resumo rápido:

1. No `labnext-caddy`: crie a rede (`docker network create caddy_net`, uma
   vez) e copie o arquivo de rotas do AgendaTEC pra dentro de `sites/`
   (`cp deploy/caddy/agendatec.caddy` do AgendaTEC pra
   `labnext-caddy/sites/agendatec.caddy`).
2. Troque o domínio na cópia que você acabou de fazer em `sites/` pra
   `localhost`, só pra esse teste, e suba o Caddy (`docker compose up -d`).
3. No AgendaTEC: descomente `COMPOSE_FILE`/`COMPOSE_PROFILES` no `.env` e
   suba (`docker compose up -d`).
4. Acesse `https://localhost/admin/` (o navegador vai avisar que o
   certificado não é confiável, é o certificado interno do Caddy, pode
   prosseguir mesmo assim).
5. Pra voltar ao normal: comente de novo as duas linhas no `.env` do
   AgendaTEC, derrube com `docker compose --profile prod down`, e no
   `labnext-caddy` substitua `sites/agendatec.caddy` por uma cópia nova do
   arquivo original (com o domínio real).

