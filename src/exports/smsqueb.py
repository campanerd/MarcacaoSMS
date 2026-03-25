import pandas as pd
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
import os

def exportar_sms_quebra(caminho_excel):

    df = pd.read_excel(caminho_excel, sheet_name="QUEBRAS")

    #input no terminal antes de criar interface
    frase_final = input("Qual a frase? ")

    #manter colunas de contrato e telefone
    df = df.iloc[:, [0, 2]]  

    # removendo telefones vazios
    df = df[df.iloc[:, 1].notna() & (df.iloc[:, 1].astype(str).str.strip() != "")]

    df["FRASEOLOGIA"] = frase_final

    # nome do arquivo
    data_str = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nome_arquivo = f"QUEBRAS_{data_str}.csv"
    destino = os.getenv("pasta_destino_quebra")
    caminho_final = os.path.join(destino, nome_arquivo)
    

    df.to_csv(caminho_final, sep=";", index=False, encoding="utf-8-sig")

    print(f"Arquivo CSV exportado: {caminho_final}")


if __name__ == "__main__":
    caminho_excel = Path.home() / "Documents" / "MarcacaoSMS" / "target" / "Quebras.xlsx"
    exportar_sms_quebra(caminho_excel)