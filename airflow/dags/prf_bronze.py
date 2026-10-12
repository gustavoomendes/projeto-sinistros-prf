from datetime import datetime, timedelta

from airflow.sdk import dag, task


@dag(
    dag_id="prf_datatran_bronze",
    description="Ingestão dos acidentes da PRF (2023-2025) na camada bronze do BigQuery",
    schedule="@monthly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["prf", "bronze"],
)
def prf_datatran_bronze():
    @task
    def carregar_bronze() -> int:
        # Import dentro da task: o Airflow faz o parse da DAG a cada ~30s
        from src.extract.bronze import carregar_bronze as carregar

        return carregar()

    carregar_bronze()


prf_datatran_bronze()
