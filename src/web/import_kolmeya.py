import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pathlib import Path


# Carrega as variáveis de ambiente
load_dotenv()

def run():
    with sync_playwright() as p:
        # Iniciando o navegador (headless=False para você ver o que está acontecendo)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Acessando a página
        page.goto("https://kolmeya.com.br/auth/login")

        # login
        page.fill('input[name="email"]', os.getenv("KOLMEYA_USER"))
        page.wait_for_timeout(100) 
        page.fill('input[name="password"]', os.getenv("KOLMEYA_PASSWORD"))
        page.keyboard.press("Enter")

        print("Login realizado!")

        page.wait_for_url("**/sms**", timeout=15000)

        # Clicando no botão de Dropdown
        page.click("a[data-bs-toggle='dropdown'].btn-success")
        page.locator(".dropdown-menu.show").get_by_text("SMS Score (short code)", exact=False).first.click()

        #Selecoes
        page.click('[name="form.files.0.segment_id"]')
        page.select_option('[name="form.files.0.segment_id"]', label="PREVENTIVO E QUEBRA")

        page.click('[name="score"]')
        page.select_option('[name="score"]', label="Média e alta probabilidade de entrega de SMS")

        page.click('[name="form.layout_id"]')
        page.select_option('[name="form.layout_id"]', label="Contrato, Telefone e Fraseologia")

        #Upload do arquivo
        file_input_selector = 'input[id="files.0.file"]'
        page.wait_for_selector(file_input_selector)

        #caminho para qualquer maquina
        base_dir = Path(__file__).resolve().parent.parent.parent
        caminho = base_dir / "target" / "QUEBRAS_LAYOUT.csv"

        #fazendo upload
        page.set_input_files(file_input_selector, caminho)
        print("Arquivo enviado!")

        btn_finish = page.locator(r'button[wire\:target="finish"]')
        btn_finish.scroll_into_view_if_needed()
        btn_finish.click()

        page.wait_for_timeout(5000)
        print("Processo concluído com sucesso!")

        # browser.close()

if __name__ == "__main__":
    run()