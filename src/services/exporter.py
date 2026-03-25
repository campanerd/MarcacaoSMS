import pandas as pd
import os
from src.repositories.conexao import get_connection

def executar_query_e_exportar(sql, nome_arquivo):
    try:
        print("Executando query...")

        with get_connection() as conn:
            df = pd.read_sql(sql, conn)

        caminho_pasta = os.getenv("pasta_destino_local")
        caminho_final = os.path.join(caminho_pasta, nome_arquivo)

        df.to_excel(caminho_final, sheet_name="QUEBRAS", index=False)

        print(f"Sucesso! {len(df)} linhas em {caminho_final}")

        return caminho_final

    except Exception as e:
        print(f"Erro: {e}")