import tempfile
from datetime import datetime, timezone
from pathlib import Path

import gdown
import pandas as pd
from google.cloud import bigquery

from src.extract import config


def ler_ano(ano: int, pasta: Path, ingested_at: datetime) -> pd.DataFrame:
    destino = pasta / f"datatran{ano}.zip"
    gdown.download(config.ARQUIVOS_PRF[ano], str(destino), quiet=True)

    df = pd.read_csv(destino, sep=config.CSV_SEP, encoding=config.CSV_ENCODING, dtype=str)
    df["_ano_arquivo"] = ano
    df["_arquivo_origem"] = destino.name
    df["_ingested_at"] = ingested_at
    print(f"{ano}: {len(df)} linhas")
    return df


def carregar_bronze() -> int:
    ingested_at = datetime.now(timezone.utc)

    with tempfile.TemporaryDirectory() as pasta:
        df = pd.concat(
            [ler_ano(ano, Path(pasta), ingested_at) for ano in config.ANOS],
            ignore_index=True,
        )

    client = bigquery.Client(project=config.GCP_PROJECT_ID, location=config.BQ_LOCATION)
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, config.BQ_TABELA_BRONZE, job_config=job_config)
    job.result()

    print(f"{job.output_rows} linhas carregadas em {config.BQ_TABELA_BRONZE}")
    return job.output_rows


if __name__ == "__main__":
    carregar_bronze()
