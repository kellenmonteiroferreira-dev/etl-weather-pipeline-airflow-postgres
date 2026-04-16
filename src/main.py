from extract_data import extract_weather_data, url
from load_data import load_weather_data
from transform_data import data_transformations
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

table_name = "sp_weather"


def pipeline():
    try:
        logging.info("Etapa 1: EXTRACT")
        data = extract_weather_data(url)

        if not data:
            raise Exception("Falha na extração: API não retornou dados")

        logging.info("Etapa 2: TRANSFORM")
        df = data_transformations()

        logging.info("Etapa 3: LOAD")
        load_weather_data(table_name, df)

        print("\n" + "=" * 60)
        print("Pipeline concluído com sucesso!")
        print("=" * 60)

    except Exception as e:
        logging.error(f"❌ ERRO no Pipeline: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    pipeline()
