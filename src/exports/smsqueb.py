import pandas as pd
from datetime import datetime
from pathlib import Path
from src.controllers.credor import buscar_telefone_por_credor
from dotenv import load_dotenv


load_dotenv()
import os

def exportar_sms_quebra(caminho_excel):

    df = pd.read_excel(caminho_excel, sheet_name="QUEBRAS")

    # mensagem base (igual VBA)
    mensagem_base = ("Nao identificamos o pagamento da sua parcela, evite apreensao do seu veiculo. Ligue: ")

    #telefone por credor
    df["TEL_CREDOR"] = df.iloc[:, 1].apply(buscar_telefone_por_credor)

    #pegar primeiro nome 
    df["PRIMEIRO_NOME"] = df.iloc[:, 3].astype(str).str.split().str[0]

    # remover telefones vazios (coluna 2) 
    df = df[df.iloc[:, 2].notna() & (df.iloc[:, 2].astype(str).str.strip() != "")]

    #montar frase 
    df["FRASEOLOGIA"] = (
        "Sr(a) " + df["PRIMEIRO_NOME"] + ", " +
        mensagem_base + " " +
        df["TEL_CREDOR"].fillna("")
    )

    # montar saída final
    df_final = pd.DataFrame({
        "CONTRATO": df.iloc[:, 0],
        "TELEFONE": df.iloc[:, 2],
        "FRASEOLOGIA": df["FRASEOLOGIA"]
    })

    data_str = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nome_arquivo = f"QUEBRAS_{data_str}.csv"

    destino = os.getenv("pasta_destino_quebra")
    caminho_final = os.path.join(destino, nome_arquivo)

    df_final.to_csv(caminho_final, sep=";", index=False, encoding="utf-8-sig")

    print(f"Arquivo CSV exportado: {caminho_final}")

    print("\nCredores sem telefone:")
    print(df[df["TEL_CREDOR"] == ""][df.columns[1]].unique())

if __name__ == "__main__":
    caminho_excel = Path.home() / "Documents" / "MarcacaoSMS" / "target" / "Quebras.xlsx"
    exportar_sms_quebra(caminho_excel)