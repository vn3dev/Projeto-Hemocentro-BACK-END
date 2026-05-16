from flask import Blueprint, jsonify
from openwith import ler_json
from datetime import date

visao_geral_bp = Blueprint('visao_geral', __name__)

TIPOS_SANGUE = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


@visao_geral_bp.get("/visao-geral")
def get_visao_geral():
    doadores = ler_json('doadores')
    bolsas   = ler_json('bolsas')
    hoje     = date.today()

    # ── Por tipo sanguíneo ────────────────────────────
    por_tipo = []
    for tipo in TIPOS_SANGUE:
        tipo_base = tipo[:-1]
        fator     = tipo[-1]

        doadores_tipo  = [d for d in doadores if d.get('tipoSangue') == tipo_base and d.get('fatorRh') == fator]
        doadores_aptos = [d for d in doadores_tipo if d.get('aptoParaDoacao')]

        bolsas_tipo   = [b for b in bolsas if b.get('tipo_sangue') == tipo]
        bolsas_validas = [b for b in bolsas_tipo if date.fromisoformat(b.get('data_validade', '1900-01-01')) >= hoje]
        total_ml       = sum(b.get('quantidade_ml', 0) for b in bolsas_validas)

        por_tipo.append({
            "tipo_sangue":     tipo,
            "total_doadores":  len(doadores_tipo),
            "doadores_aptos":  len(doadores_aptos),
            "total_bolsas":    len(bolsas_tipo),
            "bolsas_validas":  len(bolsas_validas),
            "total_ml_valido": total_ml,
        })

    # ── Totais gerais ─────────────────────────────────
    todas_validas = [b for b in bolsas if date.fromisoformat(b.get('data_validade', '1900-01-01')) >= hoje]
    totais = {
        "total_doadores":  len(doadores),
        "doadores_aptos":  sum(1 for d in doadores if d.get('aptoParaDoacao')),
        "total_bolsas":    len(bolsas),
        "bolsas_validas":  len(todas_validas),
        "total_ml_valido": sum(b.get('quantidade_ml', 0) for b in todas_validas),
    }

    # ── Últimos 5 doadores ────────────────────────────
    campos_d = ['id', 'nomeDoador', 'tipoSangue', 'fatorRh', 'sexoDoador', 'aptoParaDoacao', 'dataUltimaDoacao']
    ultimos_doadores = [{k: d.get(k) for k in campos_d} for d in doadores[-5:]][::-1]

    # ── Últimas 5 bolsas ──────────────────────────────
    campos_b = ['id', 'tipo_sangue', 'quantidade_ml', 'data_coleta', 'data_validade', 'solucao_conservante']
    ultimas_bolsas = [{k: b.get(k) for k in campos_b} for b in bolsas[-5:]][::-1]

    return jsonify({
        "por_tipo":         por_tipo,
        "totais":           totais,
        "ultimos_doadores": ultimos_doadores,
        "ultimas_bolsas":   ultimas_bolsas,
    })
