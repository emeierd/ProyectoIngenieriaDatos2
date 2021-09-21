try:
    from datetime import timedelta
    from airflow import DAG
    from datetime import datetime
    from airflow.operators.bash_operator import BashOperator

    print("All Dag modules are ok.....")
except Exception as e:
    print("Error {} ".format(e))    

# Se inicializan argumentos necesarios para Airflow
default_args= {
        "owner":"airflow",
        "retries":2,
        "retry_delay": timedelta(minutes=1)
    }

# Se inicializa el DAG, el cual será ejecutado cada 60 minutos
with DAG(
    dag_id="yapo_dag",
    schedule_interval="*/60 * * * *",
    default_args= default_args,
    start_date = datetime(2021,7,3),
    catchup=False
) as f:
    # Se crea el operador 'producer' el cual correrá el script producer.py
    yapo = BashOperator(
    task_id="yapo",
    bash_command="python3 /opt/airflow/dags/functions/yapo.py")    

# Se indica el flujo de tareas, como solo hay un operador, solo que indica 'producer'
yapo