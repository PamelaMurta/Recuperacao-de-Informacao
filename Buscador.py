

from collections import defaultdict
import math

class Buscador:
    def __init__(self, indexador):
        self.indexador = indexador

    def processar_consulta(self, consulta):
        termos = consulta.lower().split()
        resultados = defaultdict(float)
        for termo in termos:
            doc_ids = self.indexador.indice_invertido.get(termo, {})
            idf = self.indexador.idf.get(termo, 0)
            for doc_id, tf in doc_ids.items():
                resultados[doc_id] += tf * idf
        
        resultados_ordenados = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
        return resultados_ordenados

    def calcular_precisao_revocacao(self, resultados, relevantes):
        recuperados_relevantes = set(resultados) & set(relevantes)
        precisao = len(recuperados_relevantes) / len(resultados) if resultados else 0
        revocacao = len(recuperados_relevantes) / len(relevantes) if relevantes else 0
        return precisao, revocacao

    
    def classificar_resultados(self, resultados, consulta):
        scores = defaultdict(float)
        termos_consulta = consulta.lower().split()
        for termo in termos_consulta:
            doc_ids = self.indexador.buscar(termo)
            idf = self.indexador.idf.get(termo, 0)
            for doc_id, tf in doc_ids.items():
                scores[doc_id] += tf * idf
        
        resultados_ordenados = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, _ in resultados_ordenados]
