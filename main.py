from datetime import datetime
from src.queries.quebras import get_query_quebras
from src.services.exporter import executar_query_e_exportar
from src.exports.smsqueb import exportar_sms_quebra
from src.web.import_kolmeya import run as enviar_kolmeya


def rodar_quebras():
    # data teste
    data_ini = "2026-03-23 00:00:00.000"
    data_fim = "2026-03-24 00:00:00.000"

    print("Gerando base QUEBRAS...")

    #query
    sql = get_query_quebras(data_ini, data_fim)

    #exporta excel
    caminho_excel = executar_query_e_exportar(sql, "Quebras.xlsx")
    print("Gerando CSV para envio...")

    #gera CSV para kolmeya
    exportar_sms_quebra(caminho_excel)
    print("Enviando para Kolmeya...")

    
    enviar_kolmeya()
    print("Processo completo finalizado!")


def main():
    print("Iniciando automação...\n")

    rodar_quebras()

    print("\nTudo finalizado!")


if __name__ == "__main__":
    main()