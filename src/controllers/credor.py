def obter_telefones_credor():
    return {
        "Daycoval Veiculos": "1128755900",
        "Daycoval Renegociacao": "",
        "Daycoval Juridico": "1128755900",
        "Santana": "1128755903",
        "Daycoval Focos": "1128755919",
        "Santana PA": "1128755918",
        "Daycoval IFP": "1128755900",
        "Tokio Marine Ressarcimento": "",
        "Banco Digimais Amigavel": "1128755902",
        "Santana Juridico": "1128755903",
        "ICR Advogados": "",
        "Daycoval daycred": "1128755900"
    }

def buscar_telefone_por_credor(credor: str) -> str:
    telefones = obter_telefones_credor()
    return telefones.get(credor.strip(), "")