[< Voltar](../README.md) | [Documentação completa](swagger.md)

# Cheat Sheet — Hemocentro API

`Base URL: http://localhost:5000`

---

## Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/doadores` | Lista doadores |
| GET | `/doadores/<id>` | Busca doador por ID |
| POST | `/doadores` | Cria doador |
| PUT | `/doadores/<id>` | Atualiza doador (parcial) |
| DELETE | `/doadores/<id>` | Remove doador |
| GET | `/bolsas` | Lista bolsas |
| GET | `/bolsas/<id>` | Busca bolsa por ID |
| POST | `/bolsas` | Cria bolsa |
| PUT | `/bolsas/<id>` | Atualiza bolsa (parcial) |
| DELETE | `/bolsas/<id>` | Remove bolsa |
| GET | `/visao-geral` | Painel consolidado de estatísticas |

---

## Filtros (query params)

| Rota | Param | Exemplo |
|------|-------|---------|
| GET `/doadores` | `sexoDoador` | `?sexoDoador=H` |
| GET `/doadores` | `tipoSangue` | `?tipoSangue=O` |
| GET `/doadores` | `fatorRh` | `?fatorRh=%2B` |
| GET `/doadores` | `aptoParaDoacao` | `?aptoParaDoacao=true` |
| GET `/bolsas` | `tipo_sangue` | `?tipo_sangue=O%2B` |
| GET `/bolsas` | `valida` | `?valida=true` |

---

## Campos — POST /doadores

| Campo | Tipo | Obrigatório | Restrição |
|-------|------|:-----------:|-----------|
| `nomeDoador` | string | Sim | Só letras e espaços |
| `cpfDoador` | string | Sim | Único no banco |
| `telefoneDoador` | string | Sim | — |
| `sexoDoador` | string | Sim | `"H"` ou `"M"` |
| `cidadeDoador` | string | Sim | — |
| `EstadoDoador` | string | Sim | Sigla (ex.: `"SP"`) |
| `pesoDoador` | float | Sim | Positivo, em kg |
| `alturaDoador` | float | Sim | Positivo, em metros |
| `dataNascimentoDoador` | string | Sim | `YYYY-MM-DD` |
| `tipoSangue` | string | Sim | `A`, `B`, `AB`, `O` |
| `fatorRh` | string | Sim | `"+"` ou `"-"` |
| `hemoglobinaDoador` | float | Sim | Positivo, em g/dL |
| `pressaoArterialDoador` | string | Sim | `"120/80"` |
| `dataUltimaDoacao` | string | Não | `YYYY-MM-DD`; `null` se nunca doou |
| `quantidadeDoada` | integer | Não | Positivo, em ml |
| `localDoacao` | string | Não | — |
| `alergiasDoador` | string | Não | — |
| `medicamentosDoador` | string | Não | — |
| `observacoes` | string | Não | — |
| `id` | — | — | Gerado pelo servidor |
| `cadastrado` | — | — | Definido pelo servidor (`true`) |
| `aptoParaDoacao` | — | — | Calculado pelo servidor |

---

## Campos — POST /bolsas

| Campo | Tipo | Obrigatório | Restrição |
|-------|------|:-----------:|-----------|
| `tipo_sangue` | string | Sim | `A+` `A-` `B+` `B-` `AB+` `AB-` `O+` `O-` |
| `quantidade_ml` | float | Sim | Positivo, em ml |
| `data_coleta` | string | Sim | `YYYY-MM-DD`, não pode ser futura |
| `solucao_conservante` | string | Sim | `ACD` `CPD` `CPDA-1` `AS-1` `AS-3` `AS-5` |
| `id_doador` | string | Sim | — |
| `id` | — | — | Gerado pelo servidor |
| `data_validade` | — | — | Calculada pelo servidor |

**Validade por solução:** ACD/CPD → 21d · CPDA-1 → 35d · AS-1/AS-3/AS-5 → 42d

**Aptidão para doação:** Homem → 60 dias · Mulher → 90 dias desde a última doação · sem doação anterior → sempre apto

> **POST /bolsas:** ao criar uma bolsa, o servidor atualiza automaticamente `dataUltimaDoacao` e `aptoParaDoacao` do doador referenciado.

---

## GET /visao-geral

Retorna um painel consolidado. Não aceita query params.

**Campos da resposta:**

| Campo | Descrição |
|-------|-----------|
| `por_tipo[]` | Estatísticas para cada um dos 8 tipos (`A+` … `O-`) |
| `por_tipo[].total_doadores` | Doadores daquele tipo |
| `por_tipo[].doadores_aptos` | Doadores aptos daquele tipo |
| `por_tipo[].total_bolsas` | Total de bolsas daquele tipo |
| `por_tipo[].bolsas_validas` | Bolsas dentro do prazo de validade |
| `por_tipo[].total_ml_valido` | ml totais nas bolsas válidas |
| `totais` | Mesmos campos acima para todos os tipos combinados |
| `ultimos_doadores` | 5 doadores mais recentes (ordem decrescente) |
| `ultimas_bolsas` | 5 bolsas mais recentes (ordem decrescente) |

---

## Status Codes

| Código | Quando |
|--------|--------|
| `200` | GET, PUT, DELETE com sucesso |
| `201` | POST com sucesso |
| `400` | Campo ausente, nome inválido ou body vazio |
| `404` | Recurso não encontrado |
| `422` | Tipo inválido ou violação de regra de negócio |
