# Challenge B3 - Computational Thinking Using Python - Sprint 2

## Ambiente de desenvolvimento

Para realizar o setup do ambiente foi disponibilizado o arquivo `requirements.txt` contendo todas as dependencias e pacotes necessários para rodar o programa.

Utilizando o comando abaixo é possível instalar as depêndencias:

```shell
pip install -r requirements.txt
```

### Pipenv

Também é possível realizar o setup utilizando o pipenv, para isso basta utilizar o comando abaixo:

```shell
pipenv install
```

## Rodar a aplicação

Para rodar a aplicação basta utilizar os comandos abaixo:

```shell
python app.py
```

Utilizando o pipenv o comando passa a ser o abaixo:

```shell
pipenv run python app.py
```

## Usando a aplicação

### Menu principal

Abaixo o menu principal com todas as funcionalidades do sistema, para acessar elas basta digitar o código dela e pressionar `ENTER`.

```
Digite a opção desejada:
0 - Sair
1 - Cadastrar Ativo
2 - Listar Ativos
3 - Importar Preços
4 - Calcular correlação
```

### Cadastrando um ativo

Para cadastrar um ativo basta digitar o nome do ativo e o ticker dele no formato dos ticker como exibido no `Yahoo Finance`, que é a base de dados da aplicação.
Para ativos da `B3` eles em costume são apresentados como o ticker na `B3` acrescidos do sufixo `.SA`. Ex. `VALE3.SA`

```
Digite o nome do ativo: Vale S.A.
Digite o ticker do ativo: VALE3.SA
Ativo cadastrado com sucesso!
Pressione Enter para continuar
```

### Listando ativos

Para listar todos os ativos basta ir na opção desejada e uma lista com todos os ativos cadastrados será exibida conforme o exemplo:

```
Listando todos os ativos cadastrados
+----+----------+----------------+
| ID |  Ticker  |      Nome      |
+----+----------+----------------+
| 1  |   GOOG   |     Google     |
| 2  |   AAPL   |     Apple      |
| 3  |   TSLA   |     Tesla      |
| 4  | B3SA3.SA |       B3       |
| 5  | MGLU3.SA | Magazine Luiza |
| 6  | PETR3.SA |   Petrobras    |
| 7  | VALE3.SA |   Vale S.A.    |
+----+----------+----------------+
Pressione Enter para continuar
```

### Importar preços

Uma lista com todos os ativos é exibida e basta digitar o ID do ativo que deseja importar preços, em seguida digite a data de inicio da importação no formato `dd/mm/aaaa` e por fim digite a data de fim da importação, caso tenha uma entrada nula o sistema adota a data atual.

```
Listando ativos
+----+----------+-----------------+
| ID |  Ticker  |       Nome      |
+----+----------+-----------------+
| 1  |   GOOG   |      Google     |
| 2  |   AAPL   |      Apple      |
| 3  |   TSLA   |      Tesla      |
| 4  | B3SA3.SA |        B3       |
| 5  | MGLU3.SA |  Magazine Luiza |
| 6  | PETR3.SA |    Petrobras    |
| 7  | VALE3.SA |    Vale S.A.    |
| 8  | BBDC4.SA |     Bradesco    |
| 9  | BBAS3.SA | Banco do Brasil |
+----+----------+-----------------+
Selecione o ID do Ativo para importar os preços: 7
Selecione a data de inicio da importação (dd/mm/aaaa): 1/1/2022
Selecione a data final da importação ou nada para a data atual (dd/mm/aaaa): 
Importando preços, por favor aguarde...
Preços importados com sucesso!
Pressione Enter para continuar
```

### Calcular correlação entre dois ativos

Para calcular a correção basta selecionar 2 ativos entre os cadastrados para realizar o cálculo do indicador, antes disso é necessário importar os preços dos ativos.

```
Listando ativos
+----+----------+-----------------+
| ID |  Ticker  |       Nome      |
+----+----------+-----------------+
| 1  |   GOOG   |      Google     |
| 2  |   AAPL   |      Apple      |
| 3  |   TSLA   |      Tesla      |
| 4  | B3SA3.SA |        B3       |
| 5  | MGLU3.SA |  Magazine Luiza |
| 6  | PETR3.SA |    Petrobras    |
| 7  | VALE3.SA |    Vale S.A.    |
| 8  | BBDC4.SA |     Bradesco    |
| 9  | BBAS3.SA | Banco do Brasil |
+----+----------+-----------------+
Selecione o ID do primeiro ativo para calcular: 1
Selecione o ID do segundo ativo para calcular: 2
A correlação entre Google(GOOG) e Apple(AAPL) é 0.7856262281887232
Pressione Enter para continuar
```
