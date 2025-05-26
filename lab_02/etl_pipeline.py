from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Pet Store ETL Pipeline") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.1,com.clickhouse:clickhouse-jdbc:0.4.6") \
    .getOrCreate()

# Database connection parameters
PG_HOST = os.getenv("PG_HOST", "postgres")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE", "pet_store")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")

CH_HOST = os.getenv("CH_HOST", "clickhouse")
CH_PORT = os.getenv("CH_PORT", "8123")
CH_DATABASE = os.getenv("CH_DATABASE", "pet_store")
CH_USER = os.getenv("CH_USER", "default")
CH_PASSWORD = os.getenv("CH_PASSWORD", "")

try:
    # Explicitly register PostgreSQL JDBC driver
    spark._jvm.java.lang.Class.forName("org.postgresql.Driver")
except Exception as e:
    print(f"Error registering PostgreSQL driver: {e}")

def read_from_postgres(table_name):
    """Read data from PostgreSQL table"""
    return spark.read \
        .format("jdbc") \
        .option("driver", "org.postgresql.Driver") \
        .option("url", f"jdbc:postgresql://{PG_HOST}:{PG_PORT}/{PG_DATABASE}") \
        .option("dbtable", table_name) \
        .option("user", PG_USER) \
        .option("password", PG_PASSWORD) \
        .option("fetchsize", "10000") \
        .load()

def write_to_clickhouse(df, table_name):
    """Write data to ClickHouse table"""
    df.write \
        .format("jdbc") \
        .option("driver", "com.clickhouse.jdbc.ClickHouseDriver") \
        .option("url", f"jdbc:clickhouse://{CH_HOST}:{CH_PORT}/{CH_DATABASE}") \
        .option("dbtable", table_name) \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .mode("append") \
        .save()

def create_product_sales_report():
    """Create product sales report"""
    raw_data = read_from_postgres("pet_store_data")
    
    # Calculate metrics
    product_metrics = raw_data.groupBy("sale_product_id") \
        .agg(
            first("sale_product_id").cast(IntegerType()).alias("product_id"),
            first("product_name").alias("name"),
            first("product_category").alias("category"),
            sum("sale_total_price").cast(DecimalType(10, 2)).alias("total_revenue"),
            sum("sale_quantity").cast(IntegerType()).alias("total_quantity"),
            avg("product_rating").cast(DecimalType(3, 2)).alias("avg_rating"),
            sum("product_reviews").cast(IntegerType()).alias("total_reviews")
        ) \
        .select("product_id", "name", "category", "total_revenue", "total_quantity", "avg_rating", "total_reviews")
    
    # Write to ClickHouse
    write_to_clickhouse(product_metrics, "product_sales_report")

def create_customer_sales_report():
    """Create customer sales report"""
    raw_data = read_from_postgres("pet_store_data")
    
    # Calculate metrics
    customer_metrics = raw_data.groupBy("sale_customer_id") \
        .agg(
            first("sale_customer_id").cast(IntegerType()).alias("customer_id"),
            first("customer_first_name").alias("first_name"),
            first("customer_last_name").alias("last_name"),
            first("customer_country").alias("country"),
            sum("sale_total_price").cast(DecimalType(10, 2)).alias("total_spent"),
            avg("sale_total_price").cast(DecimalType(10, 2)).alias("avg_order_value"),
            count("*").cast(IntegerType()).alias("total_orders")
        ) \
        .select("customer_id", "first_name", "last_name", "country", "total_spent", "avg_order_value", "total_orders")
    
    # Write to ClickHouse
    write_to_clickhouse(customer_metrics, "customer_sales_report")

def create_time_sales_report():
    """Create time-based sales report"""
    raw_data = read_from_postgres("pet_store_data")
    
    # Add time-based columns
    time_sales = raw_data.withColumn("year", year("sale_date").cast(ShortType())) \
        .withColumn("month", month("sale_date").cast(ByteType()))
    
    # Calculate metrics
    time_metrics = time_sales.groupBy("year", "month") \
        .agg(
            sum("sale_total_price").cast(DecimalType(10, 2)).alias("monthly_revenue"),
            avg("sale_total_price").cast(DecimalType(10, 2)).alias("avg_order_value"),
            count("*").cast(IntegerType()).alias("total_orders")
        ) \
        .select("year", "month", "monthly_revenue", "avg_order_value", "total_orders")
    
    # Write to ClickHouse
    write_to_clickhouse(time_metrics, "time_sales_report")

def create_store_sales_report():
    """Create store sales report"""
    raw_data = read_from_postgres("pet_store_data")
    
    # Calculate metrics
    store_metrics = raw_data.groupBy("store_name", "store_city", "store_country") \
        .agg(
            sum("sale_total_price").cast(DecimalType(10, 2)).alias("total_revenue"),
            avg("sale_total_price").cast(DecimalType(10, 2)).alias("avg_order_value"),
            count("*").cast(IntegerType()).alias("total_orders")
        ) \
        .withColumn("store_id", monotonically_increasing_id().cast(IntegerType())) \
        .select(
            "store_id",
            col("store_name").alias("name"),
            col("store_city").alias("city"),
            col("store_country").alias("country"),
            "total_revenue",
            "avg_order_value",
            "total_orders"
        )
    
    # Write to ClickHouse
    write_to_clickhouse(store_metrics, "store_sales_report")

def create_supplier_sales_report():
    """Create supplier sales report"""
    raw_data = read_from_postgres("pet_store_data")
    
    # Calculate metrics
    supplier_metrics = raw_data.groupBy("supplier_name", "supplier_country") \
        .agg(
            sum("sale_total_price").cast(DecimalType(10, 2)).alias("total_revenue"),
            avg("product_price").cast(DecimalType(10, 2)).alias("avg_product_price"),
            count("*").cast(IntegerType()).alias("total_orders")
        ) \
        .withColumn("supplier_id", monotonically_increasing_id().cast(IntegerType())) \
        .select(
            "supplier_id",
            col("supplier_name").alias("name"),
            col("supplier_country").alias("country"),
            "total_revenue",
            "avg_product_price",
            "total_orders"
        )
    
    # Write to ClickHouse
    write_to_clickhouse(supplier_metrics, "supplier_sales_report")

def create_product_quality_report():
    """Create product quality report"""
    raw_data = read_from_postgres("pet_store_data")
    
    # Calculate metrics
    quality_metrics = raw_data.groupBy("sale_product_id") \
        .agg(
            first("sale_product_id").cast(IntegerType()).alias("product_id"),
            first("product_name").alias("name"),
            first("product_category").alias("category"),
            avg("product_rating").cast(DecimalType(3, 2)).alias("avg_rating"),
            sum("product_reviews").cast(IntegerType()).alias("total_reviews"),
            sum("sale_quantity").cast(IntegerType()).alias("total_sold"),
            sum("sale_total_price").cast(DecimalType(10, 2)).alias("total_revenue")
        ) \
        .select("product_id", "name", "category", "avg_rating", "total_reviews", "total_sold", "total_revenue")
    
    # Write to ClickHouse
    write_to_clickhouse(quality_metrics, "product_quality_report")

def main():
    """Main ETL pipeline"""
    print("Starting ETL pipeline...")
    
    # Create all reports
    print("Creating reports...")
    create_product_sales_report()
    create_customer_sales_report()
    create_time_sales_report()
    create_store_sales_report()
    create_supplier_sales_report()
    create_product_quality_report()
    
    print("ETL pipeline completed successfully!")

if __name__ == "__main__":
    main() 