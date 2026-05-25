from flask import Blueprint, jsonify, request
from openwith import ler_json, salvar_json
from datetime import date, datetime
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
    "observacoes",
    "alergiasDoador",
    "medicamentosDoador",
]

campos_numericos = [
    "pesoDoador",
    "alturaDoador",
]

campos_opcionais = [
    "alergiasDoador",
    "medicamentosDoador",
    "observacoes",
    "dataUltimaDoacao",
]

campos_editaveis = campos_obrigatorios + campos_opcionais

def validar_tamanho(data, erros_422):
    nome_doador = data.get("nomeDoador")
    if isinstance(nome_doador, str) and len(nome_doador) > 100:
        erros_422.append("nomeDoador deve conter no máximo 100 caracteres")

    cidade = data.get("cidadeDoador")
    if isinstance(cidade, str) and len(cidade) > 50:
        erros_422.append("cidadeDoador deve conter no máximo 50 caracteres")

    uf = data.get("EstadoDoador")
    if isinstance(uf, str) and len(uf) != 2:
        erros_422.append("EstadoDoador deve conter exatamente 2 caracteres")

    telefone = data.get("telefoneDoador")
    if isinstance(telefone, str) and len(telefone) > 25:
        erros_422.append("telefoneDoador deve conter no máximo 25 caracteres")

    peso_doador = data.get("pesoDoador")
    if peso_doador is not None:
        if peso_doador <= 0 or peso_doador > 300:
            erros_422.append("pesoDoador deve estar entre 1 e 300 kg")

    altura_doador = data.get("alturaDoador")
    if altura_doador is not None:
        if altura_doador <= 0 or altura_doador > 2.5:
            erros_422.append("alturaDoador deve estar entre 0.1 e 2.5 metros")

    observacoes = data.get("observacoes")
    if observacoes is not None and len(observacoes) > 500:
        erros_422.append("observacoes deve conter no máximo 500 caracteres")

    alergias = data.get("alergiasDoador")
    if alergias is not None and len(alergias) > 500:
        erros_422.append("alergiasDoador deve conter no máximo 500 caracteres")
    
    medicamentos = data.get("medicamentosDoador")
    if medicamentos is not None and len(medicamentos) > 500:
        erros_422.append("medicamentosDoador deve conter no máximo 500 caracteres")


def validar_numericos(data, erros_422):
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


def somente_digitos(cpf):
    return ''.join(caractere for caractere in (cpf or '') if caractere.isdigit())


def validar_doador(data, doadores=None):
    if doadores is None:
        doadores = []
    erros_400 = []
    erros_422 = []

    validar_numericos(data, erros_422)

    for campo in campos_obrigatorios:
        valor = data.get(campo)
        if not valor:
            erros_400.append(campo)

    for campo in campos_string:
        valor = data.get(campo)
        if valor is not None and not isinstance(valor, str):
            erros_422.append(f"{campo} deve ser uma string")

    validar_tamanho(data, erros_422)

    cpf_novo = somente_digitos(data.get('cpfDoador', ''))
    if len(cpf_novo) > 11:
        erros_422.append("cpfDoador deve conter no máximo 11 dígitos")
    if cpf_novo and any(somente_digitos(doador.get('cpfDoador', '')) == cpf_novo for doador in doadores):
        erros_422.append("cpfDoador já cadastrado")

    sexo = data.get("sexoDoador")
    if isinstance(sexo, str) and sexo:
        if sexo.upper() not in ["M", "F"]:
            erros_422.append("sexoDoador deve ser 'M' para masculino ou 'F' para feminino")
        else:
            data["sexoDoador"] = sexo.upper()

    for campo in campos_opcionais:
        data.setdefault(campo, None)

    return data, erros_400, erros_422


def validar_atualizacao_doador(data, doadores=None, id_atual=''):
    if doadores is None:
        doadores = []
    erros_400 = []
    erros_422 = []

    for campo in ["id", "aptoParaDoacao"]:
        data.pop(campo, None)

    campos_invalidos = [campo for campo in data if campo not in campos_editaveis]
    if campos_invalidos:
        erros_400.extend(campos_invalidos)

    if 'cpfDoador' in data:
        cpf_novo = somente_digitos(data.get('cpfDoador', ''))
        if cpf_novo and any(
            somente_digitos(doador.get('cpfDoador', '')) == cpf_novo and doador.get('id') != id_atual
            for doador in doadores
        ):
            erros_422.append("cpfDoador já cadastrado por outro doador")

    validar_numericos(data, erros_422)

    for campo in campos_string:
        valor = data.get(campo)
        if valor is not None and not isinstance(valor, str):
            erros_422.append(f"{campo} deve ser uma string")

    validar_tamanho(data, erros_422)

    sexo = data.get("sexoDoador")
    if isinstance(sexo, str) and sexo:
        if sexo.upper() not in ["M", "F"]:
            erros_422.append("sexoDoador deve ser 'M' para masculino ou 'F' para feminino")
        else:
            data["sexoDoador"] = sexo.upper()

    return data, erros_400, erros_422


def calcular_apto(data):
    ultima_doacao = data.get("dataUltimaDoacao")
    if not ultima_doacao:
        return True

    sexo = data.get("sexoDoador", "").upper()
    intervalo = 60 if sexo == "M" else 90
    dias_desde_ultima = (date.today() - datetime.strptime(ultima_doacao, "%Y-%m-%d").date()).days

    return dias_desde_ultima >= intervalo


@doadores_bp.get("/doadores/<id>")
def get_doador(id):
    doadores = ler_json('doadores')

    for doador in doadores:
        if doador.get('id') == id:
            return jsonify(doador)

    return jsonify({"erro": "Doador não encontrado"}), 404


@doadores_bp.get("/doadores")
def get_doadores():
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
            "erro": "Campos obrigatórios faltando",
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
