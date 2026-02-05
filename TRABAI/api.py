import requests
import random


class ServicoAPI:
    def buscar_pais_aleatorio(self):
        try:
            url = "https://restcountries.com/v3.1/all"
            resposta = requests.get(url, timeout=10)
            resposta.raise_for_status()

            dados = resposta.json()
            pais = random.choice(dados)

            nome = pais["name"]["common"]
            capital = pais.get("capital", ["Desconhecida"])[0]
            populacao = pais.get("population", 1)

            return {
                "nome": nome,
                "capital": capital,
                "populacao": populacao
            }

        except Exception as e:
            print("Erro ao chamar a API:", e)
            return None
