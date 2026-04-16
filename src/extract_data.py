import requests
import json
from pathlib import Path
import logging
from dotenv import load_dotenv
import os

# Carrega o .env da pasta config
# Carrega o .env da pasta config do Airflow
env_path = Path("/opt/airflow/config/.env")
load_dotenv(env_path)
# Carrega variáveis do arquivo .env




# Lê a chave da API do .env
api_key = os.getenv("OPENWEATHER_API_KEY")

#print("API KEY:", api_key)
# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# URL da API
#url = (
 #   f"https://api.openweathermap.org/data/2.5/weather"
  #  f"?q=Sao Paulo,BR&units=metric&appid={api_key}"
#)
# Debug temporário da chave
print("API KEY LIDA:", repr(api_key))

# URL da API
url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q=Sao Paulo,BR&units=metric&appid={api_key.strip()}"
)

print("URL GERADA:", url)

def extract_weather_data(url: str) -> dict:
    print("Iniciando extração...")

    response = requests.get(url)
    print("Status code:", response.status_code)

    # Se der erro, não salva
    if response.status_code != 200:
        logging.error("Erro na API")
        print(response.text)
        return {}

    data = response.json()
    print("Dados recebidos")

    output_path = "data/weather_data.json"
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Arquivo salvo com sucesso")
    logging.info(f"Arquivo salvo em {output_path}")

    return data


if __name__ == "__main__":
    extract_weather_data(url)




