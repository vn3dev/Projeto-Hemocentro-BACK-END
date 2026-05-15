[< Voltar](../README.md)

# Documento de Rotas

## Rotas implementadas:

### Doadores

- `GET /doadores`
    - Lista todos os doadores cadastrados, com suporte a filtros opcionais via query params.

    Query params opcionais:
    | Param | Tipo | Exemplo |
    |---|---|---|
    | `sexoDoador` | string | `H` ou `M` |
    | `tipoSangue` | string | `O` |
    | `aptoParaDoacao` | boolean | `true` |

    Body da **response**:
    ```ts
    [
        {
            "nomeDoador": "Lord Kainan, senhor das sombras",
            "cpfDoador": "123.456.789-00",
            "telefoneDoador": "(11) 98765-4321",
            "sexoDoador": "Masculino",
            "cidadeDoador": "São Paulo",
            "EstadoDoador": "SP",
            "pesoDoador": 85.5,
            "alturaDoador": 1.8,
            "dataNascimentoDoador": "2000-01-15",
            "tipoSangue": "O",
            "fatorRh": "+",
            "dataUltimaDoacao": "2024-06-01",
            "quantidadeDoada": 500,
            "localDoacao": "UCT Toledo",
            "hemoglobinaDoador": 15.2,
            "pressaoArterialDoador": "120/80",
            "alergiasDoador": "Nenhuma",
            "medicamentosDoador": "Nenhum",
            "aptoParaDoacao": true,
            "observacoes": "Doador frequente",
            "cadastrado": true,
            "id": "UUID"
        },
        ...
    ]
    ```

- `GET /doadores/<id>`
    - Busca um doador específico pelo ID. Retorna 404 se não encontrado.

    Body da **response**:
    ```ts
    {
        // mesmo schema do GET /doadores, objeto único
    }
    ```

- `POST /doadores`
    - Adiciona um novo doador. O campo `id` é gerado automaticamente (UUID) e `aptoParaDoacao` é calculado pelo servidor.

    Body da **request** com validação:
    ```ts
    {
        "nomeDoador": "string",
        "cpfDoador": "string",
        "telefoneDoador": "string",
        "sexoDoador": "string",
        "cidadeDoador": "string",
        "EstadoDoador": "string",
        "pesoDoador": 0.0,
        "alturaDoador": 0.0,
        "dataNascimentoDoador": "YYYY-MM-DD",
        "tipoSangue": "string",
        "fatorRh": "string",
        "dataUltimaDoacao": "YYYY-MM-DD",
        "quantidadeDoada": 0,
        "localDoacao": "string",
        "hemoglobinaDoador": 0.0,
        "pressaoArterialDoador": "string",
        "alergiasDoador": "string",       // opcional
        "medicamentosDoador": "string",   // opcional
        "observacoes": "string",          // opcional
        "cadastrado": true
    }
    ```

    Retorna `201` com o objeto criado, `400` se campos obrigatórios faltarem, `422` se tipos forem inválidos.

- `PUT /doadores/<id>`
    - Atualiza parcialmente os dados de um doador existente. Apenas os campos enviados no body serão alterados.

    Body da **request** (campos a atualizar):
    ```ts
    {
        "nomeDoador": "string",   // qualquer campo do schema do doador
        ...
    }
    ```

    Retorna `200` com o objeto atualizado, `404` se o doador não for encontrado.

- `DELETE /doadores/<id>`
    - Remove um doador do banco de dados pelo ID.

    Body da **response**:
    ```ts
    {
        "mensagem": "Doador deletado com sucesso"
    }
    ```

    Retorna `200` em caso de sucesso, `404` se o doador não for encontrado.

---

### Bolsas

- `GET /bolsas`
    - Lista todas as bolsas de sangue em estoque, com suporte a filtros opcionais via query params.

    Query params opcionais:
    | Param | Tipo | Exemplo |
    |---|---|---|
    | `tipo_sangue` | string | `O-` |
    | `valida` | boolean | `true` |

    Body da **response**:
    ```ts
    [
        {
            "tipo_sangue": "O-",
            "quantidade_ml": 500,
            "data_coleta": "2026-03-22",
            "solucao_conservante": "AS-1",
            "id_doador": "456",
            "id": "82427272-f82e-47cd-88cb-b9cf9396dce0",
            "data_validade": "2026-05-03"
        },
        ...
    ]
    ```

- `GET /bolsas/<id>`
    - Busca uma bolsa específica pelo ID. Retorna 404 se não encontrada.

- `POST /bolsas`
    - Adiciona uma nova bolsa ao banco. O campo `id` e `data_validade` são calculados pelo servidor.

    Body da **request** com validação:
    ```ts
    {
        "tipo_sangue": "string",
        "quantidade_ml": 0.0,
        "data_coleta": "YYYY-MM-DD",
        "solucao_conservante": "string",
        "id_doador": "string"
    }
    ```

    Retorna `201` com o objeto criado, `400` se campos obrigatórios faltarem, `422` se tipos ou datas forem inválidos.

- `PUT /bolsas/<id>`
    - Atualiza parcialmente os dados de uma bolsa existente. Apenas os campos enviados no body serão alterados.

    Body da **request** (campos a atualizar):
    ```ts
    {
        "tipo_sangue": "string",  // qualquer campo do schema da bolsa
        ...
    }
    ```

    Retorna `200` com o objeto atualizado, `404` se a bolsa não for encontrada.

- `DELETE /bolsas/<id>`
    - Remove uma bolsa do banco de dados pelo ID.

    Body da **response**:
    ```ts
    {
        "mensagem": "Bolsa deletada com sucesso"
    }
    ```

    Retorna `200` em caso de sucesso, `404` se a bolsa não for encontrada.

---

### Sangue

> **Não implementado ainda.** O blueprint `sangue` está registrado no `api.py` mas o arquivo `routes/sangue.py` ainda não existe.

- `GET /sangue/listar` *(pendente)*
    - Retornará a quantidade de cada tipo de sangue no banco.

---

## Observações

Essas foram todas as rotas implementadas até o momento. Novas rotas podem surgir conforme o projeto evolui.
