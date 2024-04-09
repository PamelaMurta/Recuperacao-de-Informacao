from collections import defaultdict
import math
import re

class Indexador:
    def __init__(self, coletor):
        self.coletor = coletor
        self.indice_invertido = defaultdict(lambda: defaultdict(int))
        self.documentos_processados = set()

    def indexar_documentos(self):
        documentos = self.coletor.obter_textos_urls()
        for url, texto in documentos:
            if url not in self.documentos_processados:
                self._indexar_texto(texto, url)
                self.documentos_processados.add(url)
        self._calcular_idf()

    def _indexar_texto(self, texto, url):
        palavras = re.findall(r'\w+', texto.lower())
        for palavra in set(palavras):
            self.indice_invertido[palavra][url] += 1

    def _calcular_idf(self):
        total_documentos = len(self.documentos_processados)
        for palavra in self.indice_invertido:
            num_documentos_com_palavra = len(self.indice_invertido[palavra])
            idf = math.log(total_documentos / num_documentos_com_palavra)
            self.indice_invertido[palavra]['idf'] = idf

    def buscar(self, termo):
        if termo in self.indice_invertido:
            return self.indice_invertido[termo]
        return []
