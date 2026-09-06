# Fluxo de trabalho com Git: branch, commit e push

Este guia apresenta o fluxo correto com boas práticas de desenvolvimento de software utilizando Git.

## Passo 1: Verificar o estado atual do repositório

```bash
git status
```

Esse comando mostra o que está diferente entre a sua pasta e o último commit: quais arquivos foram alterados, quais já estão prontos para commit e em qual branch você está. É sempre o primeiro comando a rodar antes de começar qualquer coisa, para saber de onde você está partindo.

## Passo 2: Guardar temporariamente alterações que não fazem parte da tarefa atual

```bash
git stash
```

Esse comando pega qualquer alteração que ainda não foi commitada e guarda ela de lado, deixando a pasta do jeito que estava no último commit. O terminal confirma com uma mensagem parecida com `Saved working directory and index state WIP on develop: ...`.

É útil quando você tem uma mudança em andamento que não tem nada a ver com a tarefa que está prestes a começar, evitando que ela se misture com o que vem a seguir.

Se você não tiver nenhuma alteração pendente no momento, pode pular esse passo.

## Passo 3: Atualizar a branch local com o repositório remoto

```bash
git pull
```

Esse comando baixa e aplica os commits mais recentes que outras pessoas enviaram para o repositório remoto. É importante rodar isso antes de criar uma nova branch, para garantir que o trabalho vai começar a partir da versão mais atual do projeto, evitando conflitos mais tarde.

## Passo 4: Criar uma branch nova para a alteração

```bash
git checkout -b docs/atualizacao-readme
git branch
```

O `git checkout -b` cria uma branch nova e já muda para ela em um único comando, confirmando com `Switched to a new branch '...'`. Trabalhar em uma branch separada, em vez de alterar direto a `develop`, mantém a mudança isolada até que ela seja revisada e aprovada, sem afetar o trabalho de mais ninguém enquanto isso.

O nome usado no exemplo, `docs/atualizacao-readme`, segue um padrão comum: o prefixo antes da barra (`docs`) indica o tipo de mudança (nesse caso, documentação), e o resto descreve o que está sendo feito. Troque por um nome que descreva a sua própria tarefa.

Alguns prefixos comuns, seguindo a convenção Conventional Commits:
- `feat/`: uma nova funcionalidade
- `fix/`: correção de um bug
- `docs/`: alteração em documentação
- `refactor/`: mudança no código que não corrige bug nem adiciona funcionalidade
- `test/`: adição ou ajuste de testes
- `chore/`: tarefas de manutenção que não alteram o código da aplicação

O `git branch` logo depois só lista as branches locais e marca com um `*` em qual delas você está, como conferência de que a troca deu certo.

## Passo 5: Fazer a alteração e conferir o que mudou

Com a branch criada, faça as alterações necessárias nos arquivos. Depois, confira o que mudou:

```bash
git status
```

Esse `git status` mostra os arquivos alterados e ainda não commitados, confirmando que só o que era esperado foi modificado antes de seguir para o próximo passo.

## Passo 6: Adicionar o arquivo alterado à área de staging

```bash
git add .\README.md
git status
```

O `git add` marca o arquivo como pronto para entrar no próximo commit (chamado de "staging"). Só arquivos adicionados dessa forma entram no commit, o que permite escolher exatamente o que vai junto, mesmo que existam outras alterações soltas na pasta.

O `git status` logo depois confirma que o arquivo passou para a lista "Changes to be committed", ou seja, está pronto para o commit.

## Passo 7: Criar o commit

```bash
git commit -m "docs: atualização do Readme documentando como criar a chave ssh e clonar o repositório"
```

Esse comando salva as alterações que estão na área de staging como um novo commit no histórico da branch. A mensagem depois do `-m` deve descrever o que foi feito, para que qualquer pessoa entenda a mudança só de olhar o histórico depois. Troque o texto da mensagem pela descrição da sua própria alteração.

A mensagem do exemplo já segue a convenção Conventional Commits, no formato `tipo: descrição`. Alguns exemplos com os mesmos tipos usados nos nomes de branch:
- `feat: adiciona tela de login`
- `fix: corrige erro ao salvar formulário`
- `docs: atualiza instruções de instalação`
- `refactor: simplifica função de validação`
- `test: adiciona testes para o cadastro de usuário`
- `chore: atualiza dependências do projeto`

## Passo 8: Enviar a branch para o GitHub

```bash
git push origin docs/atualizacao-readme
```

Até esse ponto, o commit existe só na sua máquina. O `git push` envia a branch, com o commit criado, para o repositório remoto no GitHub, disponibilizando ela para o restante do time. O terminal mostra algo assim:

```
remote: Create a pull request for 'docs/atualizacao-readme' on GitHub by visiting:
remote:      https://github.com/labnext-faculdade-dom-bosco/AgendaTEC/pull/new/docs/atualizacao-readme
```

Esse link é o próximo passo fora do terminal: abrir o Pull Request para que a alteração seja revisada antes de entrar na `develop`.

## Passo 9: Voltar para a branch develop

```bash
git checkout develop
git branch
```

Com a branch já enviada, o trabalho nela está feito por enquanto (o resto acontece pelo Pull Request no GitHub). O `git checkout develop` volta para a branch principal, e o `git branch` confirma que a troca deu certo.

## Passo 10: Recuperar as alterações guardadas no Passo 2

```bash
git stash pop
```

Esse comando traz de volta as alterações que tinham sido guardadas com o `git stash`, deixando elas na pasta novamente para continuar de onde parou. O terminal confirma removendo o stash da lista, com uma mensagem parecida com `Dropped refs/stash@{0} (...)`.

Se você não usou o `git stash` no Passo 2, não existe nada para recuperar aqui, e esse passo pode ser ignorado.

## Passo 11: Abrir o Pull Request no GitHub

Depois do `git push`, entre no repositório pelo navegador para abrir a página de criação do Pull Request. O GitHub mostra essa opção em um botão verde, **Compare & pull request**, logo no topo da página do repositório.

Preencha:
- **Add a title**: um título curto descrevendo a alteração (o GitHub já sugere o texto do commit).
- **Add a description**: uma descrição um pouco mais detalhada do que foi alterado e por quê.
- No painel à direita, em **Reviewers**, indique quem deve revisar a alteração.

Clique em **Create pull request**.

## Passo 12: Aguardar a aprovação

Alguém do time com permissão de revisão avalia as alterações e aprova o Pull Request. Quando isso acontece, o GitHub mostra o status **Changes approved**, junto com a confirmação de que não há conflitos com a branch base. Só depois disso o botão **Merge pull request** fica disponível.

## Passo 13: Fazer o merge e excluir a branch

Com a aprovação registrada, clique em **Merge pull request** para levar as alterações para a `develop`. O GitHub confirma que o Pull Request foi mesclado (merged) e encerrado, e libera o botão **Delete branch** para excluir a branch temporária, já que o conteúdo dela já foi incorporado à `develop`.