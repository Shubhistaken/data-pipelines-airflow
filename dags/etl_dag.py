from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.models import Variable
from operators import StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator, DataQualityOperator
from helpers import SqlQueries

# Default arguments for the DAG
default_args = {
    'owner': 'Shubham',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 31),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False
}

@dag(
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
    description='ETL pipeline for Sparkify data using Airflow and Redshift'
)
def etl_process():
    """
    ETL pipeline to extract log and song data from S3, 
    load it into Redshift staging tables, transform it, 
    and populate the analytics tables.
    """
    
    # Fetch Airflow Variables
    s3_bucket = Variable.get('s3_bucket')
    log_data_prefix = Variable.get('s3_prefix_log_data')
    song_data_prefix = Variable.get('s3_prefix_song_data')
    log_json_path_prefix = Variable.get('s3_prefix_log_json_path')
    region = Variable.get('region')

    # Start Execution
    begin_execution = EmptyOperator(task_id='Begin_execution')

    # Stage data from S3 to Redshift
    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='staging_events',
        s3_bucket=s3_bucket,
        s3_key=log_data_prefix,
        region=region,
        file_format='JSON',
        s3_json_paths_format=log_json_path_prefix
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='staging_songs',
        s3_bucket=s3_bucket,
        s3_key=song_data_prefix,
        region=region,
        file_format='JSON'
    )
    
    # Load fact table
    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id='redshift',
        table='songplays',
        sql_query=SqlQueries.songplay_table_insert
    )
    
    # Load dimension tables
    load_songs_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id='redshift',
        table='songs',
        sql_query=SqlQueries.song_table_insert
    )
    
    load_users_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id='redshift',
        table='users',
        sql_query=SqlQueries.user_table_insert
    )
    
    load_artist_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id='redshift',
        table='artists',
        sql_query=SqlQueries.artist_table_insert
    )
    
    load_time_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id='redshift',
        table='time',
        sql_query=SqlQueries.time_table_insert
    )

    # Run data quality checks
    data_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id='redshift',
        data_quality_count_checks=SqlQueries.all_data_quality_count_checks,
        data_quality_null_checks=SqlQueries.all_data_quality_null_checks
    )

    # End Execution
    end_execution = EmptyOperator(task_id='End_execution')

    # Define DAG dependencies
    begin_execution >> [stage_events_to_redshift, stage_songs_to_redshift] >> \
    load_songplays_table >> [load_songs_table, load_users_table, load_artist_table, load_time_table] >> \
    data_quality_checks >> end_execution

# Instantiate the DAG
etl_dag = etl_process()
