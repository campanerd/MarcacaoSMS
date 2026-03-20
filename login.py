import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Carrega as variáveis de ambiente
load_dotenv()

def run():
    with sync_playwright() as p:
        # 1 - Iniciando o navegador (headless=False para você ver o que está acontecendo)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 2 - Acessando a página
        page.goto("https://kolmeya.com.br/auth/login")

        # 3 - Preenchendo os campos (O Playwright já espera o elemento aparecer automaticamente)
        page.fill('input[name="email"]', os.getenv("KOLMEYA_USER"))
        page.wait_for_timeout(3) 
        page.fill('input[name="password"]', os.getenv("KOLMEYA_PASSWORD"))

        # 4 - Pressionando Enter para logar
        page.keyboard.press("Enter")

        page.wait_for_url("**/sms**", timeout=15000)

        # 5 - Clicando no botão de Dropdown
        page.click("a[data-bs-toggle='dropdown'].btn-success")
        
        page.locator(".dropdown-menu.show").get_by_text("SMS Score (short code)", exact=False).first.click()

        page.click('[name="form.files.0.segment_id"]')

        page.wait_for_timeout(100) 
        
        # browser.close()

if __name__ == "__main__":
    run()