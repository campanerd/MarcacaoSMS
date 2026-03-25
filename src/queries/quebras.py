def get_query_quebras(data_ini, data_fim):
    return f"""
    SELECT DISTINCT 
        C.CONTRATO_TIT,
        C.NOME_CRED,
        DDD_TEL + NR_TEL as TELEFONE,
        REPLACE(SUBSTRING(C.NOME_DEV, 1, CHARINDEX(' ', C.NOME_DEV, 1) -1), '" ','') AS NOME
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