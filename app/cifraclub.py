"""CifraClub Module"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

CIFRACLUB_URL = "https://www.cifraclub.com.br/"

class CifraClub():
    """CifraClub Class"""
    def __init__(self):
        options = Options()
        options.add_argument('--headless')  # Executar o navegador em modo headless (opcional)
        options.add_argument('--no-sandbox')  # Necessário em alguns ambientes como Docker
        options.add_argument('--disable-dev-shm-usage')  # Evita problemas de memória compartilhada

        self.driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=options,
            # desired_capabilities=options.to_capabilities()  # Garante compatibilidade
        )

    def cifra(self, artist: str, song: str) -> dict:
        """Lê a página HTML e extrai a cifra e meta dados da música."""
        result = {}

        url = CIFRACLUB_URL + artist + "/" + song
        result['cifraclub_url'] = url
        try:
            self.driver.get(url)
            self.get_details(result)
            self.get_cifra(result)
            self.driver.quit()
        except: # pylint: disable=bare-except
            # NoSuchElementException
            result['error'] = "error description"

        return result

    def get_details(self, result):
        """Obtêm os meta dados da música"""
        content = self.driver.find_element(By.CLASS_NAME, 'cifra').get_attribute('outerHTML')
        soup = BeautifulSoup(content, 'html.parser')
        result['name'] = soup.find('h1', class_='t1').text
        result['artist'] = soup.find('h2', class_='t3').text

        img_youtube = soup.find('div', class_='player-placeholder').img['src']
        cod = img_youtube.split('/vi/')[1].split('/')[0]
        result['youtube_url'] = f"https://www.youtube.com/watch?v={cod}"

    def get_cifra(self, result):
        """Obtêm a cifra da música e converte para json"""
        content = self.driver.find_element(By.CLASS_NAME, 'cifra_cnt').get_attribute('outerHTML')
        soup = BeautifulSoup(content, 'html.parser')
        result['cifra'] = soup.find('pre').text.split('\n')
