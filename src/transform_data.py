
import pandas as pd
from pathlib import Path
import json
import logging

# Configuração do sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Caminho do arquivo JSON
path_name = Path(__file__).parent.parent / "data" / "weather_data.json"

# Lista de colunas que serão removidas
columns_names_to_drop = ["weather", "weather_icon", "sys.type"]

# Dicionário para renomear colunas
columns_names_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "datetime",
    "timezone": "timezone",
    "id": "city_id",
    "name": "city_name",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset",
}

# Colunas para converter para datetime
columns_to_normalize_datetime = ["datetime", "sunrise", "sunset"]


def creat_dataframe(path_name: str) -> pd.DataFrame:
    """
    Lê o arquivo JSON e cria um DataFrame.
    Também normaliza a coluna weather.
    """

    def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Expande a coluna weather em colunas separadas.
        """
        df_weather = pd.json_normalize(
            df["weather"].apply(lambda x: x[0])
        )

        df_weather = df_weather.rename(columns={
            "id": "weather_id",
            "main": "weather_main",
            "description": "weather_description",
            "icon": "weather_icon"
        })

        # Junta no dataframe original
        df = pd.concat([df, df_weather], axis=1)

        logging.info(
            f"Coluna 'weather' normalizada - {len(df.columns)} colunas"
        )

        return df

    logging.info("-> Criando DataFrame do arquivo JSON...")

    path = Path(path_name)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    # Lê arquivo JSON
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Cria DataFrame
    df = pd.json_normalize(data)

    # Normaliza weather
    df = normalize_weather_columns(df)

    logging.info(f"-> DataFrame criado com {len(df)} linha(s)")

    return df


def drop_columns(df: pd.DataFrame, columns_names: list[str]) -> pd.DataFrame:
    """
    Remove colunas desnecessárias.
    Ignora colunas que não existirem no DataFrame.
    """
    logging.info(f"Removendo colunas: {columns_names}")

    df = df.drop(columns=columns_names, errors="ignore")

    logging.info(
        f"Colunas removidas - {len(df.columns)} colunas restantes"
    )

    return df

def rename_columns(df: pd.DataFrame, columns_names: dict[str, str]) -> pd.DataFrame:
    """
    Renomeia colunas para nomes mais amigáveis.
    """
    logging.info(f"Renomeando {len(columns_names)} colunas...")

    df = df.rename(columns=columns_names)

    logging.info("Colunas renomeadas")

    return df


def normalize_datetime_columns(
    df: pd.DataFrame,
    columns_names: list[str]
) -> pd.DataFrame:
    """
    Converte colunas em formato Unix timestamp
    para datetime no fuso horário de São Paulo.
    """

    # Log informando quais colunas serão convertidas
    logging.info(
        f"Convertendo colunas para datetime: {columns_names}"
    )

    # Percorre cada coluna da lista
    for name in columns_names:
        df[name] = pd.to_datetime(
            df[name],      # coluna a ser convertida
            unit="s",      # timestamp em segundos
            utc=True       # primeiro converte para UTC
        ).dt.tz_convert("America/Sao_Paulo")

    # Log de sucesso
    logging.info("Colunas convertidas para datetime")

    return df


def data_transformations() -> pd.DataFrame:
    """
    Executa toda a pipeline de transformação
    dos dados climáticos.
    """

    print("Iniciando transformações")

    # 1) Cria o dataframe a partir do JSON
    df = creat_dataframe(path_name)

    # 2) Remove colunas desnecessárias
    df = drop_columns(df, columns_names_to_drop)

    # 3) Renomeia colunas
    df = rename_columns(df, columns_names_to_rename)

    # 4) Converte timestamps em datetime
    df = normalize_datetime_columns(
        df,
        columns_to_normalize_datetime
    )

    # Log final de sucesso
    logging.info("Transformações concluídas")

    return df