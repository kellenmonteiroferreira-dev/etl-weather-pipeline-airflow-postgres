# Importa create_engine para criar conexão com banco
# text é usado para consultas SQL seguras
from sqlalchemy import create_engine, text

# quote_plus trata caracteres especiais na senha
from urllib.parse import quote_plus

# Biblioteca para variáveis de ambiente
import os

# Manipulação de caminhos
from pathlib import Path

# Pandas para DataFrame
import pandas as pd

# Carrega variáveis do arquivo .env
from dotenv import load_dotenv

# Logging para acompanhar execução
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# Lê credenciais do ambiente com valores padrão para Docker
user = os.getenv("user", "airflow")
password = os.getenv("password", "airflow")
database = os.getenv("database", "airflow")

# Host do PostgreSQL no Docker Compose
host = "postgres"


def get_engine():
    """
    Cria engine de conexão com PostgreSQL.
    """
    logging.info(f"Conectando em {host}:5432/{database}")

    return create_engine(
        f"postgresql+psycopg2://"
        f"{user}:{quote_plus(str(password))}"
        f"@{host}:5432/{database}"

    )


# Cria conexão global
engine = get_engine()


def load_weather_data(table_name: str, df: pd.DataFrame):
    """
    Carrega DataFrame para tabela PostgreSQL.
    """
    # Salva dados no banco
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )

    logging.info("Dados carregados com sucesso!")

    # Consulta para validar carga
    df_check = pd.read_sql(
        f"SELECT * FROM {table_name}",
        con=engine
    )

    logging.info(
        f"Total de registros na tabela: {len(df_check)}"
    )
