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

## 💽 Project Structure
```
data-pipelines-airflow/
│── dags/                  # Airflow DAGs
│   ├── create_tables_dag.py
│   ├── etl_dag.py
│
│── plugins/               # Custom Airflow Operators
│   ├── operators/         
│   │   ├── stage_redshift.py
│   │   ├── load_fact.py
│   │   ├── load_dimension.py
│   │   ├── data_quality.py
│   ├── helpers/           # SQL Query Helper
│   │   ├── sql_queries.py
│
│── sql/                   # SQL scripts
│   ├── create_tables.sql
│
│── docs/                  # Documentation (DAG Images)
│   ├── create_tables_dag.png
│   ├── etl_dag.png
│
│── logs/                  # Airflow logs (ignored in .gitignore)
│── .env                   # Environment variables (ignored in .gitignore)
│── README.md
```

---

## 🛠️ DAGs & Workflow
### **1️⃣ Create Tables DAG**
This DAG initializes the Redshift database by creating required tables.

![Create Tables DAG](docs/create_tables_dag.png)

### **2️⃣ ETL DAG**
This DAG performs the ETL process:
1. **Extract** logs & songs data from S3  
2. **Transform** raw data into structured analytics tables  
3. **Load** into Redshift for querying  

![ETL DAG](docs/etl_dag.png)

---

## 🚀 **Technologies Used**
- 🏠 **Apache Airflow** - Orchestration  
- ☁️ **Amazon S3** - Data Storage  
- 🔴 **Amazon Redshift** - Data Warehouse  
- 🐖 **Python** - ETL Scripts  
- 🔍 **SQL** - Data Transformation  

---

## ⚙️ **Setup Instructions**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Shubhistaken/data-pipelines-airflow.git
cd data-pipelines-airflow
```

### **2️⃣ Install Airflow & Dependencies**
```sh
pip install apache-airflow apache-airflow-providers-amazon 
```

### **3️⃣ Configure Airflow Connections**
1. **Go to Airflow UI → Admin → Connections**
2. Create a connection named **`redshift`**:
   - Conn Type: `Postgres`
   - Host: `<your-redshift-cluster-endpoint>`
   - Schema: `dev`
   - Login: `<your-db-user>`
   - Password: `<your-db-password>`
   - Port: `5439`
3. Create a connection named **`aws_credentials`**:
   - Conn Type: `Amazon Web Services`
   - Login: `Your AWS Access Key`
   - Password: `Your AWS Secret Key`

### **4️⃣ Set Airflow Variables**
Go to **Airflow UI → Admin → Variables**, and add:
| Key                     | Value |
|-------------------------|------------------------------|
| `s3_bucket`            | `shubh-airflow-project` |
| `s3_prefix_log_data`   | `log-data/` |
| `s3_prefix_song_data`  | `song-data/` |
| `s3_prefix_log_json_path` | `log-json-path.json` |
| `region`               | `us-west-2` |

### **5️⃣ Start Airflow**
```sh
airflow scheduler & airflow webserver
```

### **6️⃣ Run the DAGs**
1. Trigger `create_tables_dag` first
2. Trigger `etl_dag` next

---

## 👇 **Operators & Functionality**
| Operator | Description |
|----------|-------------|
| `StageToRedshiftOperator` | Copies raw JSON data from S3 to Redshift staging tables |
| `LoadFactOperator` | Loads data into the fact table (`songplays`) |
| `LoadDimensionOperator` | Loads data into dimension tables (`songs`, `users`, `artists`, `time`) |
| `DataQualityOperator` | Ensures row counts and NULL checks |

---

## 📄 **Data Model (Star Schema)**
```sql
-- Fact Table
songplays(songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)

-- Dimension Tables
users(user_id, first_name, last_name, gender, level)
songs(song_id, title, artist_id, year, duration)
artists(artist_id, name, location, latitude, longitude)
time(start_time, hour, day, week, month, year, weekday)
```

---

## 📚 **License**
This project is for educational purposes only.

---

## ⭐ **Contributions**
Feel free to submit issues or pull requests.

---

### **🔗 References**
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Amazon Redshift Documentation](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html)
