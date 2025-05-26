# Pet Store ETL Pipeline

This project implements an ETL pipeline using PySpark to transform data from PostgreSQL to ClickHouse, creating various analytical reports.

## Prerequisites

- Docker and Docker Compose
- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with the following content:
```env
PG_HOST=postgres
PG_PORT=5432
PG_DATABASE=pet_store
PG_USER=postgres
PG_PASSWORD=postgres

CH_HOST=clickhouse
CH_PORT=8123
CH_DATABASE=pet_store
CH_USER=default
CH_PASSWORD=
```

3. Start the services using Docker Compose:
```bash
docker-compose up -d
```

4. Wait for all services to start up (this may take a few minutes).

## Running the ETL Pipeline

To run the ETL pipeline, execute the following command:

```bash
docker exec -it lab_02-spark-1 spark-submit /opt/bitnami/spark/scripts/etl_pipeline.py
```

## Reports

The pipeline creates the following reports in ClickHouse:

1. Product Sales Report
   - Top 10 products by sales
   - Revenue by product category
   - Product ratings and reviews

2. Customer Sales Report
   - Top 10 customers by spending
   - Customer distribution by country
   - Average order value per customer

3. Time Sales Report
   - Monthly and yearly sales trends
   - Revenue comparison across periods
   - Average order size by month

4. Store Sales Report
   - Top 5 stores by revenue
   - Sales distribution by city and country
   - Average order value per store

5. Supplier Sales Report
   - Top 5 suppliers by revenue
   - Average product price by supplier
   - Sales distribution by supplier country

6. Product Quality Report
   - Products with highest/lowest ratings
   - Correlation between ratings and sales
   - Products with most reviews

## Accessing the Reports

You can access the ClickHouse database using any ClickHouse client (e.g., DBeaver) with the following connection details:
- Host: localhost
- Port: 8123
- Database: pet_store
- User: default
- Password: (empty)

## Monitoring

- Spark UI: http://localhost:8080
- ClickHouse HTTP interface: http://localhost:8123