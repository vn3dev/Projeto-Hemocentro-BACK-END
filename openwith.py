import json

def ler_json(arquivo):
    with open(f'data/{arquivo}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_json(arquivo, dados):
    with open(f'data/{arquivo}.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)