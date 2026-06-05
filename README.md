# Estrutura do projeto
```plaintext
AgendaTEC/

├── .env                 # Variáveis de ambiente (Esse arquivo nunca é enviado para o repositório!)
├── .env.example         # Exemplo das variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo git
├── Caddyfile            # Arquivo de configuração do DNS da aplicação
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
# Topologia de rede
![Topologia de rede](docker_network_topology.svg)

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

# Configurando chave SSH
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


# Configurando DNS e HTTPS
Para configurar um DNS para a aplicação e garantir que seu protocolo seja HTTPS, 
é necessário ajustar os seguintes arquivos:
- Caddyfile
- docker-compose.yml
- .env

## Caddyfile 

### Desenvolvimento local (localhost com HTTPS)

Usa certificado interno gerado pelo próprio Caddy.

```
localhost {
    tls internal
    reverse_proxy web:8000
}
```

### Produção (domínio real)

O Caddy emite e renova o certificado Let's Encrypt automaticamente.

```
meusite.com.br {
    reverse_proxy web:8000 {
        header_up X-Forwarded-Proto {scheme}
    }
}
```

`web` é o nome do serviço Django no `docker-compose.yml`.

### Configurando logs de acesso
Para configurar logs no Caddy, basta adicionar essa seção:
```
log {
    output file /data/logs/access.log {
        roll_size 10mb
        roll_keep 10
        roll_keep_for 720h
        mode 0644
    }
    format json
    level INFO
}
```
- roll_size: Tamanho de cada arquivo de log;
- rool_keep: Quantidade de arquivos de log;
- roll_keep_for: Quantidade de horas que ele mantém os registros de log (default: 30 dias);
- mode 0644: Permissão de leitura no arquivo

---

## docker-compose.yml

No `docker-compose.yml` é necessário adicionar o serviço `caddy` e garantir que todos os serviços 
que precisam se comunicar estejam na mesma rede docker.

```yaml
services:
  web:
    expose:
      - "8000"  # Não expõe a porta para o host pois o Caddy acessa internamente
    networks:
      - web

  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"    # http
      - "443:443"  # https
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data  # Armazena os certificados TLS
      - caddy_config:/config
    networks:
      - web

networks:
  web:

volumes:
  caddy_data:
  caddy_config:
```

**Importante:** todos os serviços que precisam se comunicar entre si devem estar na mesma rede (`web`). 
Sem isso, o Caddy não alcança o Django e o Django não alcança o banco.

## Variáveis de ambiente (.env)

Desenvolvimento local:

```env
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://localhost
```

Produção:

```env
DJANGO_ALLOWED_HOSTS=meusite.com.br
CSRF_TRUSTED_ORIGINS=https://meusite.com.br
```

Múltiplos valores separados por vírgula são suportados.
---

## Subindo a aplicação

```bash
docker compose up -d
```

Na primeira execução o Caddy já obtém o certificado automaticamente. Os volumes `caddy_data` e `caddy_config` devem sempre ser persistidos  sem eles os certificados são perdidos a cada restart.

---

## Desenvolvimento local  confiar no certificado

Em ambiente local com `tls internal`, o browser exibe aviso de certificado não confiável. Para resolver:

```bash
# Instala o certificado raiz do Caddy no sistema
docker compose exec caddy caddy trust
```

Reinicia o browser completamente após rodar o comando.

**Firefox** tem repositório próprio de certificados e ignora o do sistema. Exporta o certificado e importa manualmente:

```bash
docker compose cp caddy:/data/caddy/pki/authorities/local/root.crt ./caddy-root.crt
```

Depois em `about:preferences#privacy` → **Ver Certificados** → **Importar** → seleciona `caddy-root.crt` → marca "Confiar para identificar sites".

---

## Produção  pré-requisitos

Antes de subir em produção:

1. **DNS configurado**  o registro tipo `A` do domínio deve apontar para o IP do servidor
2. **Portas abertas**  80 e 443 liberadas no firewall/security group do servidor
3. **`DEBUG=False`** no `settings.py`
4. **Gunicorn** no lugar do `runserver` no docker-compose.yml:

```yaml
command: gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## Migração local → produção

É necessário alterar apenas os arquivos: `.env` e `Caddyfile`.

| Arquivo | Local | Produção |
|---|---|---|
| `Caddyfile` | `localhost { tls internal ... }` | `meusite.com.br { ... }` |
| `DJANGO_ALLOWED_HOSTS` | `localhost` | `meusite.com.br` |
| `CSRF_TRUSTED_ORIGINS` | `https://localhost` | `https://meusite.com.br` |

O Caddy cuida do certificado Let's Encrypt automaticamente  sem nenhuma configuração extra.

---

## Diagnóstico

**Verificar se o Django está acessível pelo Caddy:**
```bash
docker compose exec caddy wget -qO- http://web:8000
```

**Verificar logs do Caddy:**
```bash
docker compose logs caddy
```

**Testar HTTPS via curl:**
```bash
curl -v https://meusite.com.br
```

**Verificar se as portas estão abertas:**
```bash
curl -v http://IP_DO_SERVIDOR
curl -v https://IP_DO_SERVIDOR -k
```

Se travar no `Trying`, as portas estão bloqueadas no firewall.
