import os
from pathlib import Path

from dotenv import load_dotenv

# Local: lê o .env da raiz. No Airflow as variáveis já vêm do docker-compose
# e o load_dotenv não sobrescreve variáveis existentes.
RAIZ_PROJETO = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ_PROJETO / ".env")

# Fonte: dados abertos da PRF (acidentes agrupados por ocorrência)
ARQUIVOS_PRF = {
    2023: "https://drive.google.com/file/d/1-WO3SfNrwwZ5_l7fRTiwBKRw7mi1-HUq/view",
    2024: "https://drive.google.com/file/d/14lB0vqMFkaZj8HZ44b0njYgxs9nAN8KO/view",
    2025: "https://drive.google.com/file/d/1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR/view",
}
ANOS = sorted(ARQUIVOS_PRF)

# Leitura do CSV, definida no notebook de exploração
CSV_SEP = ";"
CSV_ENCODING = "latin-1"

# GCP
GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
BQ_LOCATION = os.environ.get("BQ_LOCATION", "US")

BQ_TABELA_BRONZE = f"{GCP_PROJECT_ID}.bronze.datatran"
