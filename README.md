The force backend.

app para venda, será possível fazer as seguintes operações:

1. cadastrar produto.
2. cadastrar cliente/fornecedor.
3. login via jwt.
4. cadastro de loja, deposito.
5. controle de estoque.
6. controle de compras.
7. controle de pedidos.

Operações devem ser desenhadas para ser usadas via API rest, usando django rest framework.

### Tarefas a fazer!

1. tirar variaveis do settings.py e apontar para o .env


### Regras!

1. regras devem estar no nível mais baixo possivel, neste caso nos models, para que seja possível usar o django admin para gerenciar os dados.
2. use o swagger para descrever as regras.
3. os dados não devem ser deletados, mas colocado a data em que foi cancelado e todos os outros objetos devem respeitar isso.


### Ideias

1. criar um middleware para controlar as requisições?