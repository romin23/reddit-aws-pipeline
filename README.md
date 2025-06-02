# 🚀 Reddit Data Engineering Pipeline on AWS

![AWS Architecture](https://via.placeholder.com/800x400.png?text=End-to-End+ETL+Pipeline)  
*End-to-End ETL Pipeline Architecture with AWS Services*

This project implements an automated data pipeline to extract, transform, and load Reddit data using Apache Airflow orchestration and AWS services. The pipeline delivers analytics-ready data to Redshift for visualization and analysis.

## 🎯 Project Goal
Create a production-grade ETL pipeline that:
1. Extracts daily posts from r/dataengineering (100 posts/day)
2. Transforms data using Python and PySpark
3. Loads to S3 data lake and Redshift data warehouse
4. Enables SQL analytics and visualization
5. Automates daily execution via Airflow

## 🛠️ Technologies Used
* **Orchestration**:  
  ![Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=flat&logo=ApacheAirflow&logoColor=white)  
  ![Celery](https://img.shields.io/badge/Celery-37814A?style=flat&logo=Celery&logoColor=white)  
  ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=Redis&logoColor=white)

* **Storage & Processing**:  
  ![S3](https://img.shields.io/badge/Amazon_S3-569A31?style=flat&logo=AmazonS3&logoColor=white)  
  ![Glue](https://img.shields.io/badge/AWS_Glue-FF9900?style=flat&logo=AmazonAWS&logoColor=white)  
  ![Redshift](https://img.shields.io/badge/Amazon_Redshift-8C4FFF?style=flat&logo=AmazonRedshift&logoColor=white)

* **Analytics**:  
  ![Athena](https://img.shields.io/badge/Amazon_Athena-1E81B0?style=flat&logo=AmazonAWS&logoColor=white)  
  ![Redshift](https://img.shields.io/badge/Redshift_Query_Editor-4051B5?style=flat&logo=AmazonRedshift&logoColor=white)

* **Development**:  
  ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white)  
  ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=Docker&logoColor=white)

## 🔄 Workflow Steps

### Extraction
- Airflow PythonOperator extracts posts using Reddit API (PRAW)

### Local Processing
- Pandas transforms data → CSV output

### S3 Loading
- Upload to `escalar-reddit-engineering/raw/`

### Glue Transformation
- PySpark job merges columns (edited+spoiler+stickied → ESS_updated)

### Data Cataloging
- Crawler creates transformed table in `reddit_db`

### Redshift Loading
- Serverless `reddit-workgroup` loads data from S3

### Analytics
Query editor enables analysis:

```sql
SELECT * FROM transformed 
WHERE title LIKE '%data stack%'
```

## 🔍 Key Implementation Details

### 📦 AWS Services Configuration

| Service       | Configuration              |
|---------------|----------------------------|
| S3 Bucket     | escalar-reddit-engineering |
| Glue Job      | reddit-glue-job            |
| Crawler       | reddit-crawler             |
| Redshift      | reddit-namespace           |
| Workgroup     | reddit-wg                  |

### 🔄 Transformation Logic

```python
# Glue PySpark Transformation
def transform_data(glueContext):
    df = glueContext.read.format("csv").load("s3://raw/")
    df = df.withColumn("ESS_updated", 
        concat(col("edited"), col("spoiler"), col("stickied")))
    return df.drop("edited", "spoiler", "stickied")
```

## 📈 Sample Analysis Output
**Comment Analysis**  
*Daily comment trends in Redshift (2024-2025)*

## ⚡ Performance Metrics

| Stage             | Duration | Data Size |
|------------------|----------|-----------|
| API Extraction   | 42s      | 1.2MB     |
| Glue Transformation | 1m 54s   | 5.86KB    |
| Athena Query     | 472ms    | -         |

## 🚀 Setup Guide

```bash
# Start Airflow cluster
docker-compose up --detach --build

# First-time setup
aws s3api create-bucket --bucket escalar-reddit-engineering
aws glue create-crawler --name reddit-crawler
aws redshift create-workgroup --workgroup-name reddit-wg
```

## 💡 Key Learnings
- Serverless AWS services reduce infrastructure management
- Glue Crawlers automate schema discovery
- Redshift Serverless provides cost-effective analytics
- Airflow+Docker enables reproducible pipelines
- Column merging significantly optimizes storage
- Data Catalog enables cross-service metadata sharing

## 📊 Future Enhancements
- Add sentiment analysis on post titles
- Implement error handling/re-try mechanisms
- Add data quality checks with Great Expectations
- Create Tableau/PowerBI dashboards
- Expand to multiple subreddits
