import pendulum
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import sql_queries

default_args = {
    "owner": "Shubham",
    "depends_on_past": False,
    "retries": 3,
}

with DAG(
    dag_id="create_tables_dag",
    default_args=default_args,
    start_date=pendulum.now(),
    schedule=None,
    catchup=False,
) as dag:

    create_artists_table = SQLExecuteQueryOperator(
        task_id="create_artists_table",
        sql=sql_queries.CREATE_ARTISTS_TABLE_SQL,
        conn_id="redshift"
    )

    create_songplays_table = SQLExecuteQueryOperator(
        task_id="create_songplays_table",
        sql=sql_queries.CREATE_SONGPLAYS_TABLE_SQL,
        conn_id="redshift"
    )

    create_songs_table = SQLExecuteQueryOperator(
        task_id="create_songs_table",
        sql=sql_queries.CREATE_SONGS_TABLE_SQL,
        conn_id="redshift"
    )

    create_time_table = SQLExecuteQueryOperator(
        task_id="create_time_table",
        sql=sql_queries.CREATE_TIME_TABLE_SQL,
        conn_id="redshift"
    )

    create_users_table = SQLExecuteQueryOperator(
        task_id="create_users_table",
        sql=sql_queries.CREATE_USERS_TABLE_SQL,
        conn_id="redshift"
    )

    create_staging_events_table = SQLExecuteQueryOperator(
        task_id="create_staging_events_table",
        sql=sql_queries.CREATE_STAGING_EVENTS_TABLE_SQL,
        conn_id="redshift"
    )

    create_staging_songs_table = SQLExecuteQueryOperator(
        task_id="create_staging_songs_table",
        sql=sql_queries.CREATE_STAGING_SONGS_TABLE_SQL,
        conn_id="redshift"
    )

    (
        create_artists_table >>
        create_songplays_table >>
        create_songs_table >>
        create_time_table >>
        create_users_table >>
        create_staging_events_table >>
        create_staging_songs_table
    )
