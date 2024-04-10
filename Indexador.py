import math
from collections import defaultdict
class Indexador:
    def __init__(self):
        self.indice_invertido = defaultdict(lambda: defaultdict(int))
        self.idf = defaultdict(float)
        self.documentos_processados = set()

    def indexar_documentos(self, textos_urls):
        for url, texto in textos_urls:
            self._indexar_texto(texto, url)
        self._calcular_idf()

    def _indexar_texto(self, texto, url):
        palavras = texto.lower().split()
        palavras_unicas = set(palavras)
        for palavra in palavras_unicas:
            self.indice_invertido[palavra][url] = palavras.count(palavra)
        self.documentos_processados.add(url)

    def _calcular_idf(self):
        total_documentos = len(self.documentos_processados)
        for palavra, docs in self.indice_invertido.items():
            num_documentos_com_palavra = len(docs)
            self.idf[palavra] = math.log(total_documentos / num_documentos_com_palavra) if num_documentos_com_palavra else 0

