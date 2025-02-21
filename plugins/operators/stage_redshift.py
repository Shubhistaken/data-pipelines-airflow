from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    copy_sql = """
        COPY {table}
        FROM '{s3_path}'
        ACCESS_KEY_ID '{access_key}'
        SECRET_ACCESS_KEY '{secret_key}'
        REGION '{region}'
        FORMAT AS {file_format}
        {json_option};
    """

    @apply_defaults
    def __init__(self, redshift_conn_id, aws_credentials_id, table, s3_bucket, s3_key, region, file_format, s3_json_paths_format=None, *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.region = region
        self.file_format = file_format
        self.s3_json_paths_format = s3_json_paths_format

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        aws_hook = S3Hook(aws_conn_id=self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        s3_path = f"s3://{self.s3_bucket}/{self.s3_key}"
        json_option = f"JSON '{self.s3_json_paths_format}'" if self.file_format == 'JSON' and self.s3_json_paths_format else "JSON 'auto'"

        formatted_sql = self.copy_sql.format(
            table=self.table,
            s3_path=s3_path,
            access_key=credentials.access_key,
            secret_key=credentials.secret_key,
            region=self.region,
            file_format=self.file_format,
            json_option=json_option
        )

        redshift.run(formatted_sql)
        self.log.info(f"Data staged to {self.table} in Redshift from {s3_path}")
