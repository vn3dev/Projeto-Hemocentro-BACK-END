# Projeto de Doação de Sangue

### 📖 [Documentação de Rotas](docs/routes.md)

###  [Documentação de Rotas - Formato Tabela](docs/routes2.md)

## Changelogs:

### [Semana 2]

Início do projeto, foi criado estrutura json de [doadores](data/doadores.json) e [sangue](data/sangue.json). Além de, algumas rotas iniciais:

- `GET /doadores/listar`
- `POST /doadores/adicionar`
- `GET /sangue/listar`

### [Semana 3]

Foram criados os diretórios [/data](data), [/routes](routes) e [/schemas](schemas) para melhor organização do projeto e separação de funções e métodos.


Foi adicionada validação para campos faltantes em [doadores](routes/doadores.py). Também foram criadas duas rotas novas:

- `GET /bolsas/listar`
- `POST /bolsas/adicionar`

A nova rota POST tem uma validação de campo faltante e atributos com valores inválidos. Ainda é necessário validação de tipagem em todas as rotas POST. Para as validações existentes, o status code correto já foi implementado.

### [Semana 4]

Nenhuma rota nova foi criada. 

Foi realizada uma revisão das rotas já existentes e dos dados que entram no sistema. Foi implementada uma verificação de presença e tipagem usando `isinstance()`. 

E também, validações específicas para os campos:

1. sexoDoador: agora só aceita "h", "H", "m" ou "M".
2. quantidade_ml: só deve aceitar numeros positivos.
3. nomeDoador: foi adicionado regex para aceitar somente letras.

Para cada erro, o sistema retorna uma mensagem personalizada e um status code adequado.

Além disso, foram adicionadas funções para tarefas especificas:

1. Calcular se o doador esta apto com base no sexo e na data da ultima doação. 
2. Calcular a data da validade da bolsa com base no tipo de conservante. 

Foram criadas tabelas de validações, como solicitado na atividade da semana 4.

###  [Tabela de Validações - Semana 4](docs/tabelas-semana4.md)

###  [Prints do Postman - Semana 4](docs/prints-semana4.md)

### [Semana 5]

Duas rotas novas foram criadas e atualizadas na [documentação](docs/routes.md) e na [tabela](docs/routes2.md)

- `GET /bolsas/<id>`
- `GET /doadores/<id>`

Para testar, utilizei id's corretos e incorretos. E registrei em [prints](docs/prints-semana5.md) da semana 5.

Além disso, algumas edições foram feitas no nome das rotas /bolsas/listar e /doadores/listar para apenas /bolsas e /doadores. Cumprindo as exigências da atividade da semana 5.
Nessas rotas, foram implementados alguns **filtros de busca**:

**Bolsas:**

1. Tipo de sangue - `GET /bolsas?tipo_sangue=A+`
2. Validade - `GET /bolsas?valida=true`

**Doadores:**

1. Sexo do doador - `GET /doadores?sexoDoador=F`
2. Tipo de sangue do doador - `GET /doadores?tipoSangue=A`
3. Apto para doação - `GET /doadores?aptoParaDoacao=true`

Os testes manuais foram evidenciados em [prints](docs/prints-semana5.md)

### [Semana 6]

A exigências da semana 6 ja haviam sido cumpridas nas outras semanas, aproveitei a entrega pra otimizar algumas partes do código e fazer melhorias que eu ja deveria ter feito.

Comecei adicionando algumas validações que estavam faltantes na rota put. Tanto de bolsas, como de doadores.

Depois disso, unifiquei as rotas /bolsas/listar com /bolsas e /doadores (existiam 2, mas com nomes de funções diferentes). Agora tem apenas /bolsas e /doadores, sem quebrar o funcionamento do código anterior.

Então, modifiquei o /docs/routes.md para manter ele atualizado.

Por fim, criei funções para abrir os jsons e substitui os open with para deixar o código mais enxuto (Ja devia ter feito isso há algumas *(muitas)* semanas 😅🤤).

Os testes manuais foram evidenciados em [prints](docs/prints-semana6.md)
