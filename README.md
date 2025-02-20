# 🚀 Data Pipelines with Apache Airflow

## 📌 Project Overview
This project builds an **ETL pipeline** for Sparkify, a music streaming service, using **Apache Airflow** and **Amazon Redshift**. It automates data ingestion, transformation, and validation for structured analytics.

### **🌟 Features**
✅ **Airflow DAGs** to orchestrate data pipeline  
✅ **Redshift Warehouse** for scalable analytics  
✅ **Custom Airflow Operators** for ETL tasks  
✅ **Data Quality Checks** to ensure integrity  
✅ **Dynamic and Reusable** pipeline  

---

## 📁 Project Structure

data-pipelines-airflow/ │── dags/ # Airflow DAGs │ ├── create_tables_dag.py │ ├── etl_dag.py │ │── plugins/ # Custom Airflow Operators │ ├── operators/
│ │ ├── stage_redshift.py │ │ ├── load_fact.py │ │ ├── load_dimension.py │ │ ├── data_quality.py │ ├── helpers/ # SQL Query Helper │ │ ├── sql_queries.py │ │── sql/ # SQL scripts │ ├── create_tables.sql │ │── docs/ # Documentation (DAG Images) │ ├── create_tables_dag.png │ ├── etl_dag.png │ │── logs/ # Airflow logs (ignored in .gitignore) │── .env # Environment variables (ignored in .gitignore) │── README.md │── .gitignore
