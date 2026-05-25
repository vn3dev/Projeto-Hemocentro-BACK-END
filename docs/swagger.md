[< Voltar](../README.md) | [Cheatsheet](cheatsheet.md)

# API Reference Hemocentro

API REST para gerenciamento de doadores e bolsas de sangue de um hemocentro.

---

## Visão Geral

| Item | Valor |
|------|-------|
| Framework | Flask (Python) |
| Porta padrão | `5000` |
| Base URL | `http://localhost:5000` |
| Formato | JSON (`Content-Type: application/json`) |
| Armazenamento | Arquivos JSON em `data/` |
| Autenticação | Nenhuma (pública) |
| CORS | Habilitado para todas as origens |

---

## Códigos de Status HTTP

| Código | Significado | Quando ocorre |
|--------|-------------|---------------|
| `200` | OK | GET, PUT e DELETE bem-sucedidos |
| `201` | Created | POST bem-sucedido — recurso criado |
| `400` | Bad Request | Campos obrigatórios ausentes, nomes de campo inválidos ou body vazio |
| `404` | Not Found | Recurso não encontrado pelo `id` informado |
| `422` | Unprocessable Entity | Tipo de dado inválido, valor fora do domínio permitido ou violação de regra de negócio |

---

## Modelos de Dados

### Doador

Representa um doador de sangue cadastrado no sistema.

| Campo | Tipo | Obrigatório | Restrições |
|-------|------|:-----------:|------------|
| `id` | string (UUID) | — | Gerado automaticamente pelo servidor |
| `nomeDoador` | string | Sim | Máximo 100 caracteres |
| `cpfDoador` | string | Sim | Deve ser único no banco; máximo 11 dígitos |
| `telefoneDoador` | string | Sim | Formato livre; máximo 25 caracteres |
| `sexoDoador` | string | Sim | Valores aceitos: `"M"` (Masculino) ou `"F"` (Feminino) |
| `cidadeDoador` | string | Sim | Máximo 50 caracteres |
| `EstadoDoador` | string | Sim | Sigla do estado com exatamente 2 caracteres (ex.: `"SP"`, `"RJ"`) |
| `pesoDoador` | float | Sim | Entre 1 e 300 kg |
| `alturaDoador` | float | Sim | Entre 0.1 e 2.5 metros |
| `dataNascimentoDoador` | string | Sim | Formato `YYYY-MM-DD` |
| `tipoSangue` | string | Sim | Ex.: `"A"`, `"B"`, `"AB"`, `"O"` |
| `fatorRh` | string | Sim | `"+"` ou `"-"` |
| `dataUltimaDoacao` | string \| null | Não | Formato `YYYY-MM-DD`; `null` se nunca doou |
| `alergiasDoador` | string \| null | Não | Máximo 500 caracteres; `null` se não informado |
| `medicamentosDoador` | string \| null | Não | Máximo 500 caracteres; `null` se não informado |
| `observacoes` | string \| null | Não | Máximo 500 caracteres; `null` se não informado |
| `cadastrado` | boolean | — | **Definido automaticamente** pelo servidor como `true` |
| `aptoParaDoacao` | boolean | — | **Calculado automaticamente** pelo servidor |

#### Regra de Aptidão para Doação

O campo `aptoParaDoacao` **não é enviado pelo cliente** — é sempre calculado com base em `dataUltimaDoacao` e `sexoDoador`:

| Sexo | Intervalo mínimo entre doações |
|------|-------------------------------|
| Masculino (`"M"`) | 60 dias |
| Feminino (`"F"`) | 90 dias |

Se `dataUltimaDoacao` for `null` (doador nunca doou), `aptoParaDoacao` é automaticamente `true`.

O valor é recalculado a cada `POST` e `PUT`. Também é recalculado automaticamente quando uma bolsa é registrada via `POST /bolsas` para o doador correspondente.

---

### Bolsa de Sangue

Representa uma bolsa coletada e armazenada no estoque.

| Campo | Tipo | Obrigatório | Restrições |
|-------|------|:-----------:|------------|
| `id` | string (UUID) | — | Gerado automaticamente pelo servidor |
| `tipo_sangue` | string | Sim | Um de: `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-` |
| `quantidade_ml` | float | Sim | Número positivo, em ml |
| `data_coleta` | string | Sim | Formato `YYYY-MM-DD` — não pode ser data futura |
| `solucao_conservante` | string | Sim | Um de: `ACD`, `CPD`, `CPDA-1`, `AS-1`, `AS-3`, `AS-5` |
| `id_doador` | string | Sim | Referência ao `id` do doador |
| `data_validade` | string | — | **Calculada automaticamente** com base em `data_coleta` + solução |

#### Validade por Solução Conservante

| Solução | Prazo de validade |
|---------|:-----------------:|
| `ACD` | 21 dias |
| `CPD` | 21 dias |
| `CPDA-1` | 35 dias |
| `AS-1` | 42 dias |
| `AS-3` | 42 dias |
| `AS-5` | 42 dias |

O campo `data_validade` é recalculado sempre que `data_coleta` ou `solucao_conservante` for alterado via `PUT`.

---

## Rotas Implementadas

---

### Doadores

---

#### `GET /doadores`

Lista todos os doadores cadastrados. Suporta filtragem opcional por query params.

**Query params (todos opcionais):**

| Param | Tipo | Valores aceitos | Exemplo |
|-------|------|-----------------|---------|
| `sexoDoador` | string | `M`, `F` | `?sexoDoador=M` |
| `tipoSangue` | string | `A`, `B`, `AB`, `O` | `?tipoSangue=O` |
| `fatorRh` | string | `+`, `-` | `?fatorRh=%2B` |
| `aptoParaDoacao` | boolean | `true`, `false` | `?aptoParaDoacao=true` |

**Response `200 OK`:**
```json
[
    {
        "id": "ace0e2ab-2ee1-4a05-82a7-ce28e5261a94",
        "nomeDoador": "Lord Kainan senhor das sombras",
        "cpfDoador": "123.456.789-00",
        "telefoneDoador": "(11) 98765-4321",
        "sexoDoador": "M",
        "cidadeDoador": "São Paulo",
        "EstadoDoador": "SP",
        "pesoDoador": 85.5,
        "alturaDoador": 1.8,
        "dataNascimentoDoador": "2000-01-15",
        "tipoSangue": "O",
        "fatorRh": "+",
        "dataUltimaDoacao": "2024-06-01",
        "alergiasDoador": null,
        "medicamentosDoador": null,
        "observacoes": null,
        "cadastrado": true,
        "aptoParaDoacao": true
    }
]
```

---

#### `GET /doadores/<id>`

Busca um doador específico pelo UUID.

**Path params:**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `id` | string (UUID) | ID do doador |

**Response `200 OK`:** objeto único com o mesmo schema acima.

**Response `404 Not Found`:**
```json
{
    "erro": "Doador não encontrado"
}
```

---

#### `POST /doadores`

Cadastra um novo doador. Os campos `id`, `cadastrado` e `aptoParaDoacao` são definidos pelo servidor e não devem ser enviados.

**Request body:**
```json
{
    "nomeDoador": "Lord Kainan senhor das sombras",
    "cpfDoador": "123.456.789-00",
    "telefoneDoador": "(11) 98765-4321",
    "sexoDoador": "M",
    "cidadeDoador": "São Paulo",
    "EstadoDoador": "SP",
    "pesoDoador": 85.5,
    "alturaDoador": 1.80,
    "dataNascimentoDoador": "2000-01-15",
    "tipoSangue": "O",
    "fatorRh": "+",
    "dataUltimaDoacao": null,
    "alergiasDoador": null,
    "medicamentosDoador": null,
    "observacoes": null
}
```

> **Nota:** campos numéricos (`pesoDoador`, `alturaDoador`) podem ser enviados como string numérica — o servidor realiza a coerção automaticamente (ex.: `"85.5"` → `85.5`).

> **Nota CPF:** a verificação de duplicidade ignora formatação — `"123.456.789-00"` e `"12345678900"` são tratados como o mesmo CPF.

**Response `201 Created`:** objeto completo com `id` (UUID gerado), `cadastrado: true` e `aptoParaDoacao` calculado.

**Response `400 Bad Request` — campos obrigatórios ausentes:**
```json
{
    "erro": "Campos obrigatorios faltando",
    "campos": ["nomeDoador", "cpfDoador"]
}
```

**Response `422 Unprocessable Entity` — validação de tipo/valor falhou:**
```json
{
    "erro": "Tipo de dado inválido",
    "campos": [
        "sexoDoador deve ser 'M' para masculino ou 'F' para feminino",
        "cpfDoador já cadastrado"
    ]
}
```

**Validações aplicadas no POST:**

| Campo | Regra |
|-------|-------|
| `nomeDoador` | Máximo 100 caracteres |
| `sexoDoador` | Deve ser exatamente `"M"` ou `"F"` (aceita minúsculas — convertido automaticamente) |
| `cpfDoador` | Não pode já existir no banco (comparação somente por dígitos); máximo 11 dígitos |
| `EstadoDoador` | Exatamente 2 caracteres |
| `cidadeDoador` | Máximo 50 caracteres |
| `telefoneDoador` | Máximo 25 caracteres |
| `pesoDoador` | Entre 1 e 300 kg |
| `alturaDoador` | Entre 0.1 e 2.5 metros |
| `alergiasDoador`, `medicamentosDoador`, `observacoes` | Máximo 500 caracteres cada |
| Todos os campos obrigatórios | Não podem estar ausentes nem vazios |

---

#### `PUT /doadores/<id>`

Atualização parcial de um doador. Apenas os campos enviados no body são alterados. Os campos `id` e `aptoParaDoacao` são ignorados mesmo se enviados.

**Path params:**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `id` | string (UUID) | ID do doador a atualizar |

**Request body** — envie somente os campos que deseja alterar:
```json
{
    "nomeDoador": "Novo Nome",
    "dataUltimaDoacao": "2025-12-01"
}
```

Após a atualização, `aptoParaDoacao` é recalculado automaticamente.

**Response `200 OK`:** objeto completo atualizado com novo `aptoParaDoacao`.

**Response `400 Bad Request` — body vazio/inválido ou campo inexistente no schema:**
```json
{
    "erro": "Campos não permitidos",
    "campos": ["campoInexistente"]
}
```

**Response `404 Not Found`:**
```json
{
    "erro": "Doador não encontrado"
}
```

**Response `422 Unprocessable Entity`:** mesmo formato do POST. A verificação de `cpfDoador` duplicado exclui o próprio doador sendo editado.

---

#### `DELETE /doadores/<id>`

Remove um doador do banco de dados pelo ID.

**Path params:**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `id` | string (UUID) | ID do doador a remover |

**Response `200 OK`:**
```json
{
    "mensagem": "Doador deletado com sucesso"
}
```

**Response `404 Not Found`:**
```json
{
    "erro": "Doador não encontrado"
}
```

---

### Bolsas de Sangue

---

#### `GET /bolsas`

Lista todas as bolsas em estoque. Suporta filtragem opcional por query params.

**Query params (todos opcionais):**

| Param | Tipo | Valores aceitos | Exemplo |
|-------|------|-----------------|---------|
| `tipo_sangue` | string | `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-` | `?tipo_sangue=O-` |
| `valida` | boolean | `true` (dentro do prazo), `false` (vencida) | `?valida=true` |

> **Atenção:** ao usar `tipo_sangue` com `+` na URL, o `+` pode ser interpretado como espaço. Prefira codificar como `%2B` (ex.: `?tipo_sangue=O%2B`) ou usar a query string diretamente (`O+` — o servidor trata a conversão internamente).

**Response `200 OK`:**
```json
[
    {
        "id": "82427272-f82e-47cd-88cb-b9cf9396dce0",
        "tipo_sangue": "O-",
        "quantidade_ml": 500,
        "data_coleta": "2026-03-22",
        "solucao_conservante": "AS-1",
        "id_doador": "ace0e2ab-2ee1-4a05-82a7-ce28e5261a94",
        "data_validade": "2026-05-03"
    }
]
```

---

#### `GET /bolsas/<id>`

Busca uma bolsa específica pelo UUID.

**Path params:**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `id` | string (UUID) | ID da bolsa |

**Response `200 OK`:** objeto único com o mesmo schema acima.

**Response `404 Not Found`:**
```json
{
    "erro": "Bolsa não encontrada"
}
```

---

#### `POST /bolsas`

Registra uma nova bolsa de sangue. Os campos `id` e `data_validade` são calculados pelo servidor.

**Request body:**
```json
{
    "tipo_sangue": "O-",
    "quantidade_ml": 450,
    "data_coleta": "2026-05-10",
    "solucao_conservante": "CPDA-1",
    "id_doador": "ace0e2ab-2ee1-4a05-82a7-ce28e5261a94"
}
```

**Response `201 Created`:** objeto completo com `id` (UUID) e `data_validade` calculada.

```json
{
    "id": "b1c2d3e4-...",
    "tipo_sangue": "O-",
    "quantidade_ml": 450,
    "data_coleta": "2026-05-10",
    "solucao_conservante": "CPDA-1",
    "id_doador": "ace0e2ab-2ee1-4a05-82a7-ce28e5261a94",
    "data_validade": "2026-06-14"
}
```

> **Efeito colateral:** ao registrar uma bolsa, o servidor atualiza automaticamente `dataUltimaDoacao` e `aptoParaDoacao` do doador referenciado em `id_doador`, caso a `data_coleta` seja mais recente que a última doação registrada.

**Response `400 Bad Request` — campos obrigatórios ausentes:**
```json
{
    "erro": "Campos obrigatorios faltando",
    "campos": ["solucao_conservante"]
}
```

**Response `422 Unprocessable Entity`:**
```json
{
    "erro": "Erros de validação",
    "campos": [
        "tipo_sangue invalido. Valores aceitos: A+, A-, B+, B-, AB+, AB-, O+, O-",
        "data_coleta não pode ser uma data futura"
    ]
}
```

**Validações aplicadas no POST:**

| Campo | Regra |
|-------|-------|
| `tipo_sangue` | Deve ser um dos 8 tipos válidos |
| `quantidade_ml` | Deve ser número positivo |
| `data_coleta` | Formato `YYYY-MM-DD` e não pode ser data futura |
| `solucao_conservante` | Deve ser um dos 6 conservantes válidos |
| `id_doador` | Não pode ser vazio |

---

#### `PUT /bolsas/<id>`

Atualização parcial de uma bolsa. Apenas os campos enviados são alterados. Os campos `id` e `data_validade` são ignorados mesmo se enviados — `data_validade` é sempre recalculada.

**Path params:**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `id` | string (UUID) | ID da bolsa a atualizar |

**Request body** — envie somente os campos que deseja alterar:
```json
{
    "solucao_conservante": "AS-5",
    "quantidade_ml": 480
}
```

Se `data_coleta` ou `solucao_conservante` forem alterados, `data_validade` é **recalculada automaticamente**.

**Response `200 OK`:** objeto completo com `data_validade` atualizada.

**Response `400 Bad Request`:**
```json
{
    "erro": "Campos não permitidos",
    "campos": ["campoInexistente"]
}
```

**Response `404 Not Found`:**
```json
{
    "erro": "Bolsa não encontrada"
}
```

**Response `422 Unprocessable Entity`:** mesmo formato do POST.

---

#### `DELETE /bolsas/<id>`

Remove uma bolsa do estoque pelo ID.

**Path params:**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `id` | string (UUID) | ID da bolsa a remover |

**Response `200 OK`:**
```json
{
    "mensagem": "Bolsa deletada com sucesso"
}
```

**Response `404 Not Found`:**
```json
{
    "erro": "Bolsa não encontrada"
}
```

---

## Resumo de Todos os Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/doadores` | Lista todos os doadores (com filtros opcionais) |
| GET | `/doadores/<id>` | Busca um doador pelo ID |
| POST | `/doadores` | Cadastra um novo doador |
| PUT | `/doadores/<id>` | Atualiza parcialmente um doador |
| DELETE | `/doadores/<id>` | Remove um doador |
| GET | `/bolsas` | Lista todas as bolsas (com filtros opcionais) |
| GET | `/bolsas/<id>` | Busca uma bolsa pelo ID |
| POST | `/bolsas` | Registra uma nova bolsa |
| PUT | `/bolsas/<id>` | Atualiza parcialmente uma bolsa |
| DELETE | `/bolsas/<id>` | Remove uma bolsa |

---

## Estrutura de Arquivos

```
Projeto-Hemocentro-BACK-END/
├── api.py               # Entrada da aplicação Flask e registro de blueprints
├── openwith.py          # Utilitários de leitura e escrita dos arquivos JSON
├── routes/
│   ├── doadores.py      # Rotas e lógica de negócio de doadores
│   └── bolsas.py        # Rotas e lógica de negócio de bolsas
├── data/
│   ├── doadores.json    # Banco de dados de doadores
│   └── bolsas.json      # Banco de dados de bolsas
└── docs/
    ├── swagger.md       # Esta documentação
    └── cheatsheet.md    # Referência rápida de rotas e campos
```
