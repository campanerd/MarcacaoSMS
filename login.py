from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

load_dotenv()

# 1 - utilizando o webDriver
options = Options()
#options.add_argument("--headless")  # opcional: roda sem abrir o navegador

driver = webdriver.Chrome(options=options)

driver.get("https://kolmeya.com.br/auth/login")

#utilizei o WebDriverWait para ter um delay, pois codigo estava bugando
wait = WebDriverWait(driver, 5)

#2 - acessando elementos numa pagina
user = wait.until(
    EC.presence_of_element_located((By.NAME, "email"))
)
user.send_keys (os.getenv("KOLMEYA_USER"))

password = wait.until(
    EC.presence_of_element_located((By.NAME, "password"))
)
password.send_keys (os.getenv("KOLMEYA_PASSWORD"))

password.send_keys(Keys.ENTER)

time.sleep(5)
# driver.quit()
