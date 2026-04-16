# ETL Weather Pipeline com Airflow + PostgreSQL + Docker

 ## Visão Geral

## Este projeto implementa um pipeline ETL automatizado utilizando Apache Airflow, Docker e PostgreSQL, com ingestão de dados da API pública OpenWeather.

O objetivo é coletar dados meteorológicos, transformá-los e armazená-los em um banco relacional de forma automatizada e agendada.


## Arquitetura do Projeto
                ┌──────────────────────┐
                │  OpenWeather API     │
                └─────────┬────────────┘
                          │ Extract
                          ▼
                ┌──────────────────────┐
                │  extract_data.py     │
                │  (Coleta JSON)       │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │ weather_data.json    │
                └─────────┬────────────┘
                          │ Transform
                          ▼
                ┌──────────────────────┐
                │ transform_data.py    │
                │ (DataFrame/Pandas)   │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │  load_data.py        │
                │ PostgreSQL (DB)      │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │ PostgreSQL Table     │
                └──────────────────────┘

        Orquestração: Apache Airflow (DAG)
        Infra: Docker Compose


 ## Tecnologias Utilizadas:
 ### Python 3.12
 ### Apache Airflow 3.x
 ### PostgreSQL 16
 ### Docker & Docker Compose
 ### OpenWeather API
 ### Pandas
 ### dotenv


## Estrutura do projeto:
airflow/
├── dags/
│   └── weather_dag.py
├── src/
│   ├── main.py
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
├── config/
│   └── .env
├── data/
│   └── weather_data.json
├── logs/
docker-compose.yaml
README.md


## Pipeline ETL:
### 1 Extract (Coleta de Dados)
Consome API OpenWeather
Retorna dados meteorológicos em JSON
Salva arquivo local weather_data.json

### 2️ Transform (Processamento)
Normaliza JSON
Remove colunas desnecessárias
Converte tipos de dados
Cria DataFrame estruturado

### 3️ Load (Carga no Banco)
Conecta no PostgreSQL via SQLAlchemy
Insere dados tratados na tabela sp_weather

## Orquestração com Airflow:
A DAG executa o pipeline diariamente:
schedule="@daily"

### Task principal:
run_weather_pipeline

### Como Executar o Projeto:
Subir containers
 docker compose up -d
 
### Acessar Airflow:
 http://localhost:8080
 
### Login padrão:
user: airflow
password: airflow

### Rodar pipeline manualmente
 docker compose exec airflow-scheduler python3 /opt/airflow/src/main.py


## Variáveis de Ambiente:

Arquivo .env:

OPENWEATHER_API_KEY=sua_chave
user=airflow
password=airflow
database=airflow

## Aprendizados:
### Construção de pipeline ETL completo
### Orquestração com Airflow
### Containerização com Docker
### Integração com API externa(OpenWeatherMap API)
### Persistência em banco relacional
### Tratamento de dados com Pandas

### - A API externa utilizada foi a OpenWeatherMap API, 
responsável por fornecer dados meteorológicos em tempo real via requisições HTTP, utilizados como fonte de dados no pipeline ETL.


### Projeto desenvolvido por Kellen Monteiro Ferreira
        
