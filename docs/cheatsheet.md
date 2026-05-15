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
| GET | `/sangue/listar` | *(pendente)* Estoque por tipo |

---

## Filtros (query params)

| Rota | Param | Exemplo |
|------|-------|---------|
| GET `/doadores` | `sexoDoador` | `?sexoDoador=H` |
| GET `/doadores` | `tipoSangue` | `?tipoSangue=O` |
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
| `dataUltimaDoacao` | string | Sim | `YYYY-MM-DD` |
| `quantidadeDoada` | integer | Sim | Positivo, em ml |
| `localDoacao` | string | Sim | — |
| `hemoglobinaDoador` | float | Sim | Positivo, em g/dL |
| `pressaoArterialDoador` | string | Sim | `"120/80"` |
| `cadastrado` | boolean | Sim | — |
| `alergiasDoador` | string | Não | — |
| `medicamentosDoador` | string | Não | — |
| `observacoes` | string | Não | — |
| `id` | — | — | Gerado pelo servidor |
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

**Aptidão para doação:** Homem → 60 dias · Mulher → 90 dias desde a última doação

---

## Status Codes

| Código | Quando |
|--------|--------|
| `200` | GET, PUT, DELETE com sucesso |
| `201` | POST com sucesso |
| `400` | Campo ausente, nome inválido ou body vazio |
| `404` | Recurso não encontrado |
| `422` | Tipo inválido ou violação de regra de negócio |
