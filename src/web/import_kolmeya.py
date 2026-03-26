import os
from time import sleep
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

        #caminho para qualquer maquina
        base_dir = Path(__file__).resolve().parent.parent.parent
        caminho = base_dir / "target" / "QUEBRAS_LAYOUT.csv"

        file_input = page.locator(r'#files\.0\.file')

        print("Inputs encontrados antes:", file_input.count())

        file_input.set_input_files(str(caminho))
        print("Arquivo enviado")

        print("Logo após upload:",
            file_input.evaluate("el => el.files && el.files.length ? el.files[0].name : null"))

        page.wait_for_timeout(3000)

        novo_input = page.locator(r'#files\.0\.file')

        print("Inputs encontrados depois:", novo_input.count())
        print("3s depois:",
            novo_input.evaluate("el => el.files && el.files.length ? el.files[0].name : null"))

        page.screenshot(path="debug_upload.png", full_page=True)

        file_input.set_input_files(str(caminho))
        print("Arquivo enviado")

        print("Logo após upload:",
            file_input.evaluate("el => el.files && el.files.length ? el.files[0].name : null"))

        page.wait_for_timeout(3000)

        novo_input = page.locator(r'#files\.0\.file')

        print("Inputs encontrados depois:", novo_input.count())
        print("3s depois:",
            novo_input.evaluate("el => el.files && el.files.length ? el.files[0].name : null"))


        sleep(20)

        page.wait_for_function("""
        () => {
            const input = document.querySelector('#files\\\\.0\\\\.file');
            return input && input.files.length > 0;
        }
    """)

        btn_finish = page.locator('button:has-text("criar")')


        btn_finish.wait_for(state="visible")
        btn_finish.wait_for(state="attached")

        page.wait_for_timeout(2000)  # pequeno buffer (opcional)

        btn_finish.click()
        print("Processo concluído com sucesso!")

        sleep(20)

        page.wait_for_function("""
        () => {
            const input = document.querySelector('#files\\\\.0\\\\.file');
            return input && input.files.length > 0;
        }
    """)

        btn_finish = page.locator('button:has-text("criar")')


        btn_finish.wait_for(state="visible")
        btn_finish.wait_for(state="attached")

        page.wait_for_timeout(2000)  # pequeno buffer (opcional)

        btn_finish.click()
        print("Processo concluído com sucesso!")

        # browser.close()

if __name__ == "__main__":
    run()