import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO)

class Coletor:
    def __init__(self, urls, max_depth=2):
        self.urls = urls
        self.max_depth = max_depth
        self.visited_urls = set()
        self.textos_urls = []
        self.session = requests.Session()
        self.session.max_redirects = 20
        self.iniciar_coleta()

    def iniciar_coleta(self):
        for url in self.urls:
            self._coletar_url(url, depth=0)

    def _coletar_url(self, url, depth):
        if depth > self.max_depth or url in self.visited_urls:
            return
        self.visited_urls.add(url)
        try:
            response = self.session.get(url, allow_redirects=True)
            final_url = response.url  # Considera o URL final após redirecionamentos.
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                texto = self._extrair_texto(soup)
                links = self._extrair_links(soup, final_url)
                
                self.textos_urls.append((final_url, texto))
                
                for link in links:
                    if self._filtro_link(link) and link not in self.visited_urls:
                        self._coletar_url(link, depth + 1)
            else:
                logging.error(f"Acesso negado a {url} com status code: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Erro ao acessar {url}: {e}")

    def _extrair_texto(self, soup):
        tags_interessantes = ['h1', 'h2', 'h3', 'p', 'li']
        texto = "\n".join(tag.get_text(strip=True) for tag in soup.find_all(tags_interessantes))
        return texto

    def _extrair_links(self, soup, base_url):
        links = [urljoin(base_url, link['href']) for link in soup.find_all('a', href=True) if 'http' in link['href']]
        return links

    def _filtro_link(self, link):
        # Assegura que apenas links dentro do contexto definido sejam coletados.
        return any(link.startswith(url) for url in self.urls)

    def obter_textos_urls(self):
        return self.textos_urls

