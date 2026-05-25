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

---

## Filtros (query params)

| Rota | Param | Exemplo |
|------|-------|---------|
| GET `/doadores` | `sexoDoador` | `?sexoDoador=M` |
| GET `/doadores` | `tipoSangue` | `?tipoSangue=O` |
| GET `/doadores` | `fatorRh` | `?fatorRh=%2B` |
| GET `/doadores` | `aptoParaDoacao` | `?aptoParaDoacao=true` |
| GET `/bolsas` | `tipo_sangue` | `?tipo_sangue=O%2B` |
| GET `/bolsas` | `valida` | `?valida=true` |

---

## Campos — POST /doadores

| Campo | Tipo | Obrigatório | Restrição |
|-------|------|:-----------:|-----------|
| `nomeDoador` | string | Sim | Máximo 100 caracteres |
| `cpfDoador` | string | Sim | Único no banco; máximo 11 dígitos |
| `telefoneDoador` | string | Sim | Máximo 25 caracteres |
| `sexoDoador` | string | Sim | `"M"` (Masculino) ou `"F"` (Feminino) |
| `cidadeDoador` | string | Sim | Máximo 50 caracteres |
| `EstadoDoador` | string | Sim | Exatamente 2 caracteres (ex.: `"SP"`) |
| `pesoDoador` | float | Sim | Entre 1 e 300 kg |
| `alturaDoador` | float | Sim | Entre 0.1 e 2.5 metros |
| `dataNascimentoDoador` | string | Sim | `YYYY-MM-DD` |
| `tipoSangue` | string | Sim | Ex.: `A`, `B`, `AB`, `O` |
| `fatorRh` | string | Sim | `"+"` ou `"-"` |
| `dataUltimaDoacao` | string | Não | `YYYY-MM-DD`; `null` se nunca doou |
| `alergiasDoador` | string | Não | Máximo 500 caracteres |
| `medicamentosDoador` | string | Não | Máximo 500 caracteres |
| `observacoes` | string | Não | Máximo 500 caracteres |
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

**Aptidão para doação:** Masculino (`"M"`) → 60 dias · Feminino (`"F"`) → 90 dias desde a última doação · sem doação anterior → sempre apto

> **POST /bolsas:** ao criar uma bolsa, o servidor atualiza automaticamente `dataUltimaDoacao` e `aptoParaDoacao` do doador referenciado.

---

## Status Codes

| Código | Quando |
|--------|--------|
| `200` | GET, PUT, DELETE com sucesso |
| `201` | POST com sucesso |
| `400` | Campo ausente, nome inválido ou body vazio |
| `404` | Recurso não encontrado |
| `422` | Tipo inválido ou violação de regra de negócio |
