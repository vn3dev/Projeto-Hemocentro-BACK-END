from flask import Blueprint, jsonify, request
from openwith import ler_json, salvar_json
from datetime import datetime, timedelta, date
import uuid

bolsas_bp = Blueprint('bolsas', __name__)

tipos_sangue_validos = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

validade_por_solucao = {
    "ACD": 21,
    "CPD": 21,
    "CPDA-1": 35,
    "AS-1": 42,
    "AS-3": 42,
    "AS-5": 42,
}

campos_obrigatorios = [
    "tipo_sangue",
    "quantidade_ml",
    "data_coleta",
    "solucao_conservante",
    "id_doador"
]

campos_string = [
    "tipo_sangue",
    "data_coleta",
    "solucao_conservante"
]

campos_numericos = ["quantidade_ml"]

campos_editaveis = campos_obrigatorios


def validar_bolsa(bolsa):
    erros_400 = []
    erros_422 = []

    for campo in campos_obrigatorios:
        if campo not in bolsa or bolsa[campo] == "" or bolsa[campo] is None:
            erros_400.append(campo)

    if bolsa.get("tipo_sangue") not in tipos_sangue_validos:
        erros_422.append("tipo_sangue invalido. Valores aceitos: A+, A-, B+, B-, AB+, AB-, O+, O-")

    for campo in campos_string:
        valor = bolsa.get(campo)
        if valor is not None and not isinstance(valor, str):
            erros_422.append(f"{campo} deve ser uma string")

    for campo in campos_numericos:
        valor = bolsa.get(campo)
        if valor is not None and not isinstance(valor, (int, float)):
            erros_422.append(f"{campo} deve ser um número")

    quantidade = bolsa.get("quantidade_ml")
    if isinstance(quantidade, (int, float)) and quantidade <= 0 and not None:
        erros_422.append("quantidade_ml deve ser um número positivo")

    return bolsa, erros_400, erros_422


def validar_atualizacao_bolsa(bolsa):
    erros_400 = []
    erros_422 = []

    for campo in ["id", "data_validade"]:
        bolsa.pop(campo, None)

    campos_invalidos = [c for c in bolsa if c not in campos_editaveis]
    if campos_invalidos:
        erros_400.extend(campos_invalidos)

    for campo in campos_string:
        valor = bolsa.get(campo)
        if valor is not None and not isinstance(valor, str):
            erros_422.append(f"{campo} deve ser uma string")

    for campo in campos_numericos:
        valor = bolsa.get(campo)
        if valor is not None and not isinstance(valor, (int, float)):
            erros_422.append(f"{campo} deve ser um número")

    tipo_sangue = bolsa.get("tipo_sangue")
    if tipo_sangue is not None and tipo_sangue not in tipos_sangue_validos:
        erros_422.append("tipo_sangue invalido. Valores aceitos: A+, A-, B+, B-, AB+, AB-, O+, O-")

    quantidade = bolsa.get("quantidade_ml")
    if isinstance(quantidade, (int, float)) and quantidade <= 0:
        erros_422.append("quantidade_ml deve ser um número positivo")

    return bolsa, erros_400, erros_422


def calcular_validade(bolsa):
    solucao_conservante = bolsa["solucao_conservante"]

    if solucao_conservante not in validade_por_solucao:
        erro = "Solução conservante '" + solucao_conservante + "' não reconhecida. Valores aceitos: ACD, CPD, CPDA-1, AS-1, AS-3, AS-5"
        return bolsa, erro

    dias_validade = validade_por_solucao[solucao_conservante]

    try:
        data_coleta = datetime.strptime(bolsa["data_coleta"], "%Y-%m-%d")
    except ValueError:
        return bolsa, "data_coleta inválida. Use o formato YYYY-MM-DD"

    hoje = datetime.now()
    if data_coleta > hoje:
        return bolsa, "data_coleta não pode ser uma data futura"

    data_validade = data_coleta + timedelta(days=dias_validade)
    bolsa["data_validade"] = data_validade.strftime("%Y-%m-%d")

    return bolsa, None


@bolsas_bp.get("/bolsas/<id>")
def get_bolsa(id):
    bolsas = ler_json('bolsas')

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            return jsonify(bolsa)

    return jsonify({"erro": "Bolsa não encontrada"}), 404


@bolsas_bp.get("/bolsas")
def get_bolsas():
    bolsas = ler_json('bolsas')

    tipo_sangue = request.args.get('tipo_sangue', '').replace(' ', '+') or None
    valida = request.args.get('valida')

    resultado = []

    for bolsa in bolsas:
        if tipo_sangue and bolsa.get('tipo_sangue') != tipo_sangue:
            continue
        if valida is not None:
            data_validade = date.fromisoformat(bolsa.get('data_validade'))
            eh_valida = data_validade >= date.today()
            if (valida.lower() == 'true') != eh_valida:
                continue
        resultado.append(bolsa)

    return jsonify(resultado)


@bolsas_bp.put("/bolsas/<id>")
def atualizar(id):
    bolsas = ler_json('bolsas')

    dados = request.get_json(force=True, silent=True)
    if not dados:
        return jsonify({"erro": "Body da requisição inválido ou ausente"}), 400

    dados, erros_400, erros_422 = validar_atualizacao_bolsa(dados)
    if erros_400:
        return jsonify({
            "erro": "Campos não permitidos",
            "campos": erros_400
        }), 400
    if erros_422:
        return jsonify({
            "erro": "Erros de validação",
            "campos": erros_422
        }), 422

    for bolsa in bolsas:
        if bolsa.get('id') == id:
            bolsa.update(dados)
            if "data_coleta" in dados or "solucao_conservante" in dados:
                bolsa, erro = calcular_validade(bolsa)
                if erro:
                    return jsonify({"erro": erro}), 422
            salvar_json('bolsas', bolsas)
            return jsonify(bolsa), 200

    return jsonify({"erro": "Bolsa não encontrada"}), 404


@bolsas_bp.delete("/bolsas/<id>")
def deletar(id):
    bolsas = ler_json('bolsas')

    for i, bolsa in enumerate(bolsas):
        if bolsa.get('id') == id:
            del bolsas[i]
            salvar_json('bolsas', bolsas)
            return jsonify({"mensagem": "Bolsa deletada com sucesso"}), 200

    return jsonify({"erro": "Bolsa não encontrada"}), 404


@bolsas_bp.post("/bolsas")
def add_bolsa():
    nova_bolsa = request.json
    nova_bolsa['id'] = str(uuid.uuid4())

    nova_bolsa, erros_400, erros_422 = validar_bolsa(nova_bolsa)
    if erros_400:
        return jsonify({
            "erro": "Campos obrigatórios faltando",
            "campos": erros_400
        }), 400
    if erros_422:
        return jsonify({
            "erro": "Erros de validação",
            "campos": erros_422
        }), 422

    nova_bolsa, erro = calcular_validade(nova_bolsa)
    if erro:
        return jsonify({"erro": erro}), 422

    bolsas = ler_json('bolsas')
    bolsas.append(nova_bolsa)
    salvar_json('bolsas', bolsas)

    return jsonify(nova_bolsa), 201
