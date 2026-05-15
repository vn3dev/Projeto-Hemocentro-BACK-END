import json

# funções pra trocar os openwith por uma função

# recebe o nome do arquivo e retorna o conteúdo do json como uma lista ou dict
def ler_json(arquivo: str) -> list | dict:
    with open(f'data/{arquivo}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# recebe o nome do arquivo e os dados python a serem salvos, não retorna nada
def salvar_json(arquivo: str, dados: list | dict) -> None:
    with open(f'data/{arquivo}.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)