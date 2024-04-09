import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO)

class Coletor:
    def __init__(self, urls, max_depth=2):
        self.urls = urls
        self.visited_urls = set()
        self.max_depth = max_depth  
        self.textos_urls = []
        self.session = requests.Session() 

    def coletar(self):
        for url in self.urls:
            self._coletar_url(url, depth=0)

    def _coletar_url(self, url, depth):
        if depth > self.max_depth or url in self.visited_urls:
            return
        try:
            response = self.session.get(url)
            # Atualização para usar response.text e permitir que 'requests' lide com a decodificação
            soup = BeautifulSoup(response.text, 'html.parser')
            texto = self._extrair_texto(soup)
            links = self._extrair_links(soup, url)
            
            self.textos_urls.append((url, texto))  
            
            for link in links:
                if self._filtro_link(link) and link not in self.visited_urls:
                    self._coletar_url(link, depth + 1)  

        except requests.RequestException as e:
            logging.error(f"Erro ao acessar {url}: {e}")

    def _extrair_texto(self, soup):
        texto = "\n".join(tag.get_text() for tag in soup.find_all(['p', 'h1']))
        return texto

    def _extrair_links(self, soup, base_url):
        links = [urljoin(base_url, link['href']) for link in soup.find_all('a', href=True)]
        return links

    def _filtro_link(self, link):
        return any(link.startswith(url) for url in self.urls)

    def obter_textos_urls(self):
        return self.textos_urls

