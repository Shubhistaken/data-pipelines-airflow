from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self, redshift_conn_id, data_quality_count_checks, data_quality_null_checks, *args, **kwargs):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.data_quality_count_checks = data_quality_count_checks
        self.data_quality_null_checks = data_quality_null_checks

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for check in self.data_quality_count_checks:
            records = redshift.get_records(check["sql"])
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed: {check['sql']} returned no results")
            if records[0][0] < check["expected_result"]:
                raise ValueError(f"Data quality check failed: {check['sql']} expected at least {check['expected_result']}, got {records[0][0]}")
            self.log.info(f"Data quality check passed: {check['sql']} returned {records[0][0]}")

        for check in self.data_quality_null_checks:
            records = redshift.get_records(check["sql"])
            if records[0][0] > check["expected_result"]:
                raise ValueError(f"Data quality check failed: {check['sql']} expected {check['expected_result']} nulls, got {records[0][0]}")
            self.log.info(f"Data quality check passed: {check['sql']} returned {records[0][0]}")
