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
| `nomeDoador` | string | Sim | Apenas letras e espaços (sem números ou especiais) |
| `cpfDoador` | string | Sim | Deve ser único no banco |
| `telefoneDoador` | string | Sim | Formato livre |
| `sexoDoador` | string | Sim | Valores aceitos: `"H"` (Homem) ou `"M"` (Mulher) |
| `cidadeDoador` | string | Sim | — |
| `EstadoDoador` | string | Sim | Sigla do estado (ex.: `"SP"`, `"RJ"`) |
| `pesoDoador` | float | Sim | Número positivo, em kg |
| `alturaDoador` | float | Sim | Número positivo, em metros |
| `dataNascimentoDoador` | string | Sim | Formato `YYYY-MM-DD` |
| `tipoSangue` | string | Sim | Ex.: `"A"`, `"B"`, `"AB"`, `"O"` |
| `fatorRh` | string | Sim | `"+"` ou `"-"` |
| `dataUltimaDoacao` | string | Sim | Formato `YYYY-MM-DD` |
| `quantidadeDoada` | integer | Sim | Quantidade em ml (número positivo) |
| `localDoacao` | string | Sim | Nome do local da última doação |
| `hemoglobinaDoador` | float | Sim | Nível de hemoglobina em g/dL |
| `pressaoArterialDoador` | string | Sim | Formato `"###/##"` (ex.: `"120/80"`) |
| `alergiasDoador` | string \| null | Não | `null` se não informado |
| `medicamentosDoador` | string \| null | Não | `null` se não informado |
| `observacoes` | string \| null | Não | `null` se não informado |
| `cadastrado` | boolean | Sim | Status de cadastro |
| `aptoParaDoacao` | boolean | — | **Calculado automaticamente** pelo servidor |

#### Regra de Aptidão para Doação

O campo `aptoParaDoacao` **não é enviado pelo cliente** — é sempre calculado com base em `dataUltimaDoacao` e `sexoDoador`:

| Sexo | Intervalo mínimo entre doações |
|------|-------------------------------|
| Homem (`"H"`) | 60 dias |
| Mulher (`"M"`) | 90 dias |

O valor é recalculado a cada `POST` e `PUT`.

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
| `sexoDoador` | string | `H`, `M` | `?sexoDoador=H` |
| `tipoSangue` | string | `A`, `B`, `AB`, `O` | `?tipoSangue=O` |
| `aptoParaDoacao` | boolean | `true`, `false` | `?aptoParaDoacao=true` |

**Response `200 OK`:**
```json
[
    {
        "id": "ace0e2ab-2ee1-4a05-82a7-ce28e5261a94",
        "nomeDoador": "Lord Kainan senhor das sombras",
        "cpfDoador": "123.456.789-00",
        "telefoneDoador": "(11) 98765-4321",
        "sexoDoador": "H",
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

Cadastra um novo doador. Os campos `id` e `aptoParaDoacao` são gerados pelo servidor e não devem ser enviados.

**Request body:**
```json
{
    "nomeDoador": "Lord Kainan senhor das sombras",
    "cpfDoador": "123.456.789-00",
    "telefoneDoador": "(11) 98765-4321",
    "sexoDoador": "H",
    "cidadeDoador": "São Paulo",
    "EstadoDoador": "SP",
    "pesoDoador": 85.5,
    "alturaDoador": 1.80,
    "dataNascimentoDoador": "2000-01-15",
    "tipoSangue": "O",
    "fatorRh": "+",
    "dataUltimaDoacao": "2024-06-01",
    "quantidadeDoada": 500,
    "localDoacao": "UCT Toledo",
    "hemoglobinaDoador": 15.2,
    "pressaoArterialDoador": "120/80",
    "cadastrado": true,
    "alergiasDoador": null,
    "medicamentosDoador": null,
    "observacoes": null
}
```

**Response `201 Created`:** objeto completo com `id` (UUID gerado) e `aptoParaDoacao` calculado.

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
        "sexoDoador deve ser 'H' ou 'M'",
        "cpfDoador já cadastrado"
    ]
}
```

**Validações aplicadas no POST:**

| Campo | Regra |
|-------|-------|
| `nomeDoador` | Apenas letras e espaços (regex `^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$`) |
| `sexoDoador` | Deve ser exatamente `"H"` ou `"M"` |
| `cpfDoador` | Não pode já existir no banco |
| `pesoDoador`, `alturaDoador`, `hemoglobinaDoador`, `quantidadeDoada` | Devem ser números positivos |
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
    "hemoglobinaDoador": 16.0,
    "dataUltimaDoacao": "2025-12-01"
}
```

Após a atualização, `aptoParaDoacao` é recalculado automaticamente.

**Response `200 OK`:** objeto completo atualizado com novo `aptoParaDoacao`.

**Response `400 Bad Request` — body vazio ou campo inexistente no schema:**
```json
{
    "erro": "Campos inválidos",
    "campos": ["campoInexistente"]
}
```

**Response `404 Not Found`:**
```json
{
    "erro": "Doador não encontrado"
}
```

**Response `422 Unprocessable Entity`:** mesmo formato do POST.

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
    "erro": "Tipo de dado inválido",
    "campos": [
        "tipo_sangue inválido. Use: A+, A-, B+, B-, AB+, AB-, O+, O-",
        "data_coleta não pode ser futura"
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
    "erro": "Campos inválidos",
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

### Sangue *(não implementado)*

> O blueprint `sangue` está registrado em `api.py`, mas o arquivo `routes/sangue.py` ainda não existe. A aplicação **não iniciará** enquanto essa rota estiver importada e o arquivo estiver ausente.

| Endpoint | Descrição |
|----------|-----------|
| `GET /sangue/listar` | Retornará o resumo do estoque por tipo sanguíneo |

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
| GET | `/sangue/listar` | *(pendente)* Resumo do estoque por tipo |

---

## Estrutura de Arquivos

```
Projeto-Hemocentro-BACK-END/
├── api.py               # Entrada da aplicação Flask e registro de blueprints
├── openwith.py          # Utilitários de leitura e escrita dos arquivos JSON
├── routes/
│   ├── doadores.py      # Rotas e lógica de negócio de doadores
│   ├── bolsas.py        # Rotas e lógica de negócio de bolsas
│   └── sangue.py        # (pendente) Rotas de resumo de estoque
├── data/
│   ├── doadores.json    # Banco de dados de doadores
│   └── bolsas.json      # Banco de dados de bolsas
└── docs/
    ├── swagger.md       # Esta documentação
    └── table_rotas.md   # Tabela de referência rápida de rotas
```
