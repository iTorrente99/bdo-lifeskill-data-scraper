import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils import extract_profile_info

class Scraper:
    def __init__(self):
        self.driver = self.set_driver()

    def set_driver(self):
        """Inicializa el navegador y lo minimiza."""
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.minimize_window()
        return driver

    def get_guild_raw(self, guildName, region="EU", retries=5):
        """Obtiene la lista de miembros de una guild y sus perfiles con reintentos en caso de error."""
        url = f"https://www.naeu.playblackdesert.com/en-US/Adventure/Guild/GuildProfile?guildName={guildName}&region={region}"
        attempt = 0
        while attempt < retries:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "box_list_area")))
                # Obtener el HTML
                box_list_area = self.driver.find_element(By.CLASS_NAME, "box_list_area")
                html_data = box_list_area.get_attribute('innerHTML')

                # Parsear el HTML
                soup = BeautifulSoup(html_data, 'html.parser')
                members = {}
                for li in soup.find_all('li'):
                    a_tags = li.find_all('a')
                    for a_tag in a_tags:
                        family_name = a_tag.text.strip()
                        profile_url = a_tag['href']
                        if family_name and profile_url:
                            members[family_name] = profile_url

                members_data = self.get_members_data(members)
                return members_data
            except Exception as e:
                print(f"No se encontró el elemento para la URL: {url}. Intento {attempt + 1} de {retries}. Error: {e}")
                attempt += 1
                #time.sleep(2)  # Esperar 2 segundos antes de reintentar
                if attempt == retries:
                    print(f"Se agotaron los intentos para la URL: {url}.")
                    return {}

    def get_members_data(self, members, retries=5):
        """Obtiene los datos de cada miembro de la guild con reintentos en caso de error."""
        members_data = {}
        for family_name, profile_url in members.items():
            attempt = 0
            while attempt < retries:
                try:
                    self.driver.get(profile_url)
                    WebDriverWait(self.driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "box_profile_area")))
                    box_profile_area = self.driver.find_element(By.CLASS_NAME, "box_profile_area")
                    html_data = box_profile_area.get_attribute('innerHTML')
                    members_data[family_name] = extract_profile_info(html_data)
                    members_data[family_name]['profile_url'] = profile_url
                    break  # Salir del bucle si la carga es exitosa
                except Exception as e:
                    print(f"No se encontró el elemento para la URL: {profile_url}. Intento {attempt + 1} de {retries}. Error: {e}")
                    attempt += 1
                    #time.sleep(2)  # Esperar 2 segundos antes de reintentar
                    if attempt == retries:
                        print(f"Se agotaron los intentos para la URL: {profile_url}.")
        
        return members_data

    def close(self):
        self.driver.quit()
