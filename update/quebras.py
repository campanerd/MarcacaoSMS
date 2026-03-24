import os

import pyodbc
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def atualizar_quebras():
    data_ini = "2025-10-01 00:00:00.000" 
    data_fim = "2025-10-02 23:59:59.998" 

    conn_str = (
        "Driver={SQL Server};"
        "Server=192.168.1.219;"
        "Database=Mailing;"
        "Trusted_Connection=yes;"
    )

    sql = f"""
    SELECT DISTINCT 
        C.CONTRATO_TIT,
        C.NOME_CRED,
        DDD_TEL + NR_TEL as TELEFONE,
        REPLACE(SUBSTRING(C.NOME_DEV, 1, CHARINDEX(' ', C.NOME_DEV, 1) -1), '" ','') AS NOME,
        (SELECT TOP 1 BE.DataVencimento 
         FROM [192.168.0.143].cobsystems3.dbo.BOLETOS_EM BE  
         WHERE BE.COD_TIT = A.COD_TIT  
         ORDER BY BE.DATAVENCIMENTO DESC) AS ULTIMO__VENC
    FROM [192.168.0.143].cobsystems3.dbo.BOLETOS_EM A WITH(NOLOCK)
    LEFT JOIN [192.168.0.143].cobsystems3.dbo.RECEBIMENTOS B WITH(NOLOCK)
        ON A.Cod_BEm = B.COD_BEM
    INNER JOIN [192.168.0.143].cobreports.dbo.posicao_carteira C WITH(NOLOCK)
        ON A.Cod_Tit = C.COD_TIT
    INNER JOIN [192.168.0.143].cobsystems3.dbo.V_DEVEDORES D WITH(NOLOCK)
        ON C.CPFCGC_PES = D.CPFCGC_PES COLLATE Latin1_General_CI_AI
    INNER JOIN [192.168.0.143].cobsystems3.dbo.PESSOAS_TELEFONES E WITH(NOLOCK)
        ON D.COD_PES = E.COD_PES
    WHERE A.DATAVENCIMENTO BETWEEN '{data_ini}' AND '{data_fim}'
        AND B.COD_REC IS NULL 
        AND (USUARIO_CANC IS NULL OR USUARIO_CANC=1000)
        AND DDD_TEL <> ''
        AND DDD_TEL IS NOT NULL
        AND LEFT(NR_TEL, 1) = '9'
        AND LEN(NR_TEL) = 9
        AND STATUS_TEL IN (3)
        AND C.COD_CRED IN (1,3,4,5,9,12,15,16,18)
        AND (SELECT TOP 1 CAST(BE.DataVencimento AS DATE) 
             FROM [192.168.0.143].cobsystems3.dbo.BOLETOS_EM BE 
             WHERE BE.COD_TIT = A.COD_TIT 
             ORDER BY BE.DATAVENCIMENTO DESC) < CAST(GETDATE() AS DATE)
    """

    try:
        # Execução
        print("Conectando ao banco e executando query...")
        with pyodbc.connect(conn_str, timeout=0) as conn:
            df = pd.read_sql(sql, conn)

        caminho_pasta = os.getenv("pasta_destino_local")


        nome_arquivo = f"Quebras.xlsx"

        caminho_final = os.path.join( caminho_pasta, nome_arquivo)

        df.to_excel(caminho_final, sheet_name="QUEBRAS", index=False)
        
        print(f"Sucesso! {len(df)} linhas importadas para {caminho_final}")

    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == "__main__":
    atualizar_quebras()