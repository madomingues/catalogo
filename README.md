# Catálogo de cerveja

    Aplicativo Web utilizado para listar e descrever tipos de cerveja, cevejas e
    suas características.

## Pré - requisitos

    Para essa ferramenta foi utilizado a linguagem python versão 2.7.12, o orm 
    sqlAlchemy e o acesso para o aplicativo web foi utilizado o programa Git Bash
    versão 2.7.4., e para acessar o conteúdo personalizado é necessário conta no
    Google.

## Guia de utilização

    O objetivo dessa ferramenta é catalogar tipos de cerveja, cervejas e suas 
    características, sendo que usuários com contas podem adicionar, remover, e
    editar conteúdo.

    O  catálogo de cervejas pode ser acessado:
    [1000 Cervejas] (http://localhost:8000/1000cervejas)
    Para acessar o catálogo utilizar o git Bash e abrir a pasta em que está o 
    catálogo através do comando cd, nessa pasta digitar o comando python 
    db_setup.py para iniciar o banco de dados e  python project.py para iniciar
    o servidor.

    Para acessar o aplicativo web, abrir o navegador e digitar o link acima.

#### Tabelas do banco de dados News

    O banco de dados cervejas.db é composto por três tabelas, de usuários, de 
    tipos de cerveja e de cerveja.

###### Tabela Users

A tabela users é composta pelas colunas:
* id: tipo integer e chave primária
* name: tipo string 
* email: tipo string

###### Tabela BeerStyle

A tabela BeerStyle é composta pelas colunas:
* name: tipo string
* descricao: tipo string
* id: tipo integer e é chave primária

###### Tabela Cerveja

A tabela Cerveja é composta pelas colunas:
* name: tipo string
* tipo: tipo string
* cor: tipo string
* temperatura: tipo string
* familia: tipo string
* preco:tipo string
* descricao:tipo string
* id: tipo integer e é a chave primária

#### Funcionalidades

Para usuários com conta no 1000 cervejas é possível adicionar items, editar e 
deletar.

## Autoria

Esse projeito foi feito por Marla Domingues para a Udacity.
