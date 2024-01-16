Aplicação em Python/FastApi utilizando Docker, docker-compose, Postgres, SQLALchemy, Migrations com Alembic e Pytest. O projeto é desenvolvido utilizando a metodologia TDD (Test Driven Development).
Disponibiliza uma API REST para manipulação de uma base de dados, contendo esta, um modelo de dados de usuário e um modelo de dados de salários. Cada usuário pode ter uma ou mais entradas de salário no
mês. As informações do usuário que a API retorna contém algumas informações calculadas dinamicamente.
O modelo de usuário é composto por cpf, nome e data de nascimento. Já o modelo de dados de salário armazena a data, o salário e os descontos.
As seguintes informações de usuário são disponibilizadas via API, além das contidas na base de dados:
- A média dos salários
- A média dos descontos
- O maior salário
- O menor salário
A aplicação possui os endpoints /users e /salaries com as operações CRUD via API REST.

