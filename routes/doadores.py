from flask import Blueprint, jsonify, request
from openwith import ler_json, salvar_json
from datetime import date, datetime
import re
import uuid

doadores_bp = Blueprint('doadores', __name__)

campos_obrigatorios = [
    "nomeDoador",
    "cpfDoador",
    "telefoneDoador",
    "sexoDoador",
    "cidadeDoador",
    "EstadoDoador",
    "pesoDoador",
    "alturaDoador",
    "dataNascimentoDoador",
    "tipoSangue",
    "fatorRh",
    "hemoglobinaDoador",
    "pressaoArterialDoador",
]

campos_string = [
    "nomeDoador",
    "cpfDoador",
    "telefoneDoador",
    "sexoDoador",
    "cidadeDoador",
    "EstadoDoador",
    "dataNascimentoDoador",
    "tipoSangue",
    "fatorRh",
    "dataUltimaDoacao",
    "localDoacao",
    "pressaoArterialDoador",
    "observacoes"
]

campos_numericos = [
    "pesoDoador",
    "alturaDoador",
    "quantidadeDoada",
    "hemoglobinaDoador"
]

campos_opcionais = [
    "alergiasDoador",
    "medicamentosDoador",
    "observacoes",
    "dataUltimaDoacao",
    "quantidadeDoada",
    "localDoacao",
]

campos_editaveis = campos_obrigatorios + campos_opcionais


def calcular_apto(data):
    ultima_doacao = data.get("dataUltimaDoacao")
    if not ultima_doacao:
        return True

    sexo = data.get("sexoDoador", "").upper()
    intervalo = 60 if sexo == "H" else 90
    dias_desde_ultima = (date.today() - datetime.strptime(ultima_doacao, "%Y-%m-%d").date()).days

    return dias_desde_ultima >= intervalo


def coagir_numericos(data, erros_422):
    """Converte campos numéricos enviados como string para float (comportamento do Angular)."""
    for campo in campos_numericos:
        valor = data.get(campo)
        if valor is None:
            continue
        if isinstance(valor, str):
            if valor.strip() == '':
                data[campo] = None
            else:
                try:
                    data[campo] = float(valor)
                except ValueError:
                    erros_422.append(f"{campo} deve ser um número")
        elif not isinstance(valor, (int, float)):
            erros_422.append(f"{campo} deve ser um número")


def _somente_digitos(cpf):
    return re.sub(r'\D', '', cpf or '')


def validar_doador(data, doadores=[]):
    erros_400 = []
    erros_422 = []

    coagir_numericos(data, erros_422)

    for campo in campos_obrigatorios:
        valor = data.get(campo)
        if not valor:
            erros_400.append(campo)

    cpf_novo = _somente_digitos(data.get('cpfDoador', ''))
    if cpf_novo and any(_somente_digitos(d.get('cpfDoador', '')) == cpf_novo for d in doadores):
        erros_422.append("cpfDoador já cadastrado")

    for campo in campos_string:
        valor = data.get(campo)
        if valor is not None and not isinstance(valor, str):
            erros_422.append(f"{campo} deve ser uma string")

    nome = data.get("nomeDoador")
    if isinstance(nome, str) and nome and not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome):
        erros_422.append("nomeDoador não deve conter números ou caracteres especiais")

    sexo = data.get("sexoDoador")
    if isinstance(sexo, str) and sexo:
        if sexo.upper() not in ["H", "M"]:
            erros_422.append("sexoDoador deve ser 'H' para homem ou 'M' para mulher")

    for campo in campos_opcionais:
        data.setdefault(campo, None)

    return data, erros_400, erros_422


def validar_atualizacao_doador(data, doadores=[], id_atual=''):
    erros_400 = []
    erros_422 = []

    for campo in ["id", "aptoParaDoacao"]:
        data.pop(campo, None)

    campos_invalidos = [c for c in data if c not in campos_editaveis]
    if campos_invalidos:
        erros_400.extend(campos_invalidos)

    if 'cpfDoador' in data:
        cpf_novo = _somente_digitos(data.get('cpfDoador', ''))
        if cpf_novo and any(
            _somente_digitos(d.get('cpfDoador', '')) == cpf_novo and d.get('id') != id_atual
            for d in doadores
        ):
            erros_422.append("cpfDoador já cadastrado por outro doador")

    coagir_numericos(data, erros_422)

    for campo in campos_string:
        valor = data.get(campo)
        if valor is not None and not isinstance(valor, str):
            erros_422.append(f"{campo} deve ser uma string")

    nome = data.get("nomeDoador")
    if isinstance(nome, str) and nome and not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome):
        erros_422.append("nomeDoador não deve conter números ou caracteres especiais")

    sexo = data.get("sexoDoador")
    if isinstance(sexo, str) and sexo and sexo.upper() not in ["H", "M"]:
        erros_422.append("sexoDoador deve ser 'H' para homem ou 'M' para mulher")

    return data, erros_400, erros_422


@doadores_bp.get("/doadores/<id>")
def get_doador(id):
    doadores = ler_json('doadores')

    for doador in doadores:
        if doador.get('id') == id:
            return jsonify(doador)

    return jsonify({"erro": "Doador não encontrado"}), 404


@doadores_bp.get("/doadores")
def get_doadores(id=None):
    doadores = ler_json('doadores')

    sexo        = request.args.get('sexoDoador')
    tipo_sangue = request.args.get('tipoSangue')
    fator_rh    = request.args.get('fatorRh')
    apto        = request.args.get('aptoParaDoacao')

    resultado = []

    for doador in doadores:
        if sexo        and doador.get('sexoDoador') != sexo:
            continue
        if tipo_sangue and doador.get('tipoSangue') != tipo_sangue:
            continue
        if fator_rh    and doador.get('fatorRh') != fator_rh:
            continue
        if apto is not None:
            apto_bool = apto.lower() == 'true'
            if doador.get('aptoParaDoacao') != apto_bool:
                continue
        resultado.append(doador)

    return jsonify(resultado)


@doadores_bp.put("/doadores/<id>")
def atualizar(id):
    doadores = ler_json('doadores')

    dados = request.get_json(force=True, silent=True)
    if not dados:
        return jsonify({"erro": "Body da requisição inválido ou ausente"}), 400

    dados, erros_400, erros_422 = validar_atualizacao_doador(dados, doadores, id)
    if erros_400:
        return jsonify({
            "erro": "Campos não permitidos",
            "campos": erros_400
        }), 400
    if erros_422:
        return jsonify({
            "erro": "Tipo de dado inválido",
            "campos": erros_422
        }), 422

    for doador in doadores:
        if doador.get('id') == id:
            doador.update(dados)
            doador['aptoParaDoacao'] = calcular_apto(doador)
            salvar_json('doadores', doadores)
            return jsonify(doador), 200

    return jsonify({"erro": "Doador não encontrado"}), 404


@doadores_bp.delete("/doadores/<id>")
def deletar(id):
    doadores = ler_json('doadores')

    for i, doador in enumerate(doadores):
        if doador.get('id') == id:
            del doadores[i]
            salvar_json('doadores', doadores)
            return jsonify({"mensagem": "Doador deletado com sucesso"}), 200

    return jsonify({"erro": "Doador não encontrado"}), 404


@doadores_bp.post("/doadores")
def add_doador():
    novo_doador = request.get_json(force=True, silent=True)
    if not novo_doador:
        return jsonify({"erro": "Body da requisição inválido ou ausente"}), 400
    novo_doador['id'] = str(uuid.uuid4())
    novo_doador['cadastrado'] = True

    doadores = ler_json('doadores')

    novo_doador, erros_400, erros_422 = validar_doador(novo_doador, doadores)
    if erros_400:
        return jsonify({
            "erro": "Campos obrigatorios faltando",
            "campos": erros_400
        }), 400
    if erros_422:
        return jsonify({
            "erro": "Tipo de dado inválido",
            "campos": erros_422
        }), 422

    novo_doador['aptoParaDoacao'] = calcular_apto(novo_doador)
    doadores.append(novo_doador)
    salvar_json('doadores', doadores)

    return jsonify(novo_doador), 201
