import re

def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""
    
    # remove espaços extras e padroniza
    texto = texto.strip().lower()
    texto = re.sub(r"\s+", " ", texto)  # remove espaços duplos
    
    return texto

def obter_telefones_credor():
    return {
        "daycoval veiculos": "1128755900",
        "daycoval renegociacao": "",
        "daycoval juridico": "1128755900",
        "santana": "1128755903",
        "daycoval focos": "1128755919",
        "santana pa": "1128755918",
        "daycoval ifp": "1128755900",
        "tokio marine ressarcimento": "",
        "banco digimais amigavel": "1128755902",
        "santana juridico": "1128755903",
        "icr advogados": "",
        "daycoval daycred": "1128755900"
    }

def buscar_telefone_por_credor(credor: str) -> str:
    telefones = obter_telefones_credor()

    credor_normalizado = normalizar_texto(credor)

    telefones_normalizados = {
        normalizar_texto(k): v for k, v in telefones.items()
    }

    return telefones_normalizados.get(credor_normalizado, "")