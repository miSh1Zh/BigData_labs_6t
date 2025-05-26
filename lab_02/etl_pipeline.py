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
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE", "pet_store")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")

CH_HOST = os.getenv("CH_HOST", "localhost")
CH_PORT = os.getenv("CH_PORT", "8123")
CH_DATABASE = os.getenv("CH_DATABASE", "pet_store")
CH_USER = os.getenv("CH_USER", "default")
CH_PASSWORD = os.getenv("CH_PASSWORD", "")

def read_from_postgres(table_name):
    """Read data from PostgreSQL table"""
    return spark.read \
        .format("jdbc") \
        .option("url", f"jdbc:postgresql://{PG_HOST}:{PG_PORT}/{PG_DATABASE}") \
        .option("dbtable", table_name) \
        .option("user", PG_USER) \
        .option("password", PG_PASSWORD) \
        .load()

def write_to_clickhouse(df, table_name):
    """Write data to ClickHouse table"""
    df.write \
        .format("jdbc") \
        .option("url", f"jdbc:clickhouse://{CH_HOST}:{CH_PORT}/{CH_DATABASE}") \
        .option("dbtable", table_name) \
        .option("user", CH_USER) \
        .option("password", CH_PASSWORD) \
        .mode("overwrite") \
        .save()

def create_product_sales_report():
    """Create product sales report"""
    sales_df = read_from_postgres("sales")
    products_df = read_from_postgres("products")
    
    # Join sales with products
    product_sales = sales_df.join(products_df, "product_id")
    
    # Calculate metrics
    product_metrics = product_sales.groupBy("product_id", "name", "category") \
        .agg(
            sum("total_price").alias("total_revenue"),
            sum("quantity").alias("total_quantity"),
            avg("rating").alias("avg_rating"),
            sum("reviews").alias("total_reviews")
        )
    
    # Get top 10 products by sales
    top_products = product_metrics.orderBy(desc("total_quantity")).limit(10)
    
    # Write to ClickHouse
    write_to_clickhouse(product_metrics, "product_sales_report")

def create_customer_sales_report():
    """Create customer sales report"""
    sales_df = read_from_postgres("sales")
    customers_df = read_from_postgres("customers")
    
    # Join sales with customers
    customer_sales = sales_df.join(customers_df, "customer_id")
    
    # Calculate metrics
    customer_metrics = customer_sales.groupBy("customer_id", "first_name", "last_name", "country") \
        .agg(
            sum("total_price").alias("total_spent"),
            avg("total_price").alias("avg_order_value"),
            count("*").alias("total_orders")
        )
    
    # Get top 10 customers
    top_customers = customer_metrics.orderBy(desc("total_spent")).limit(10)
    
    # Write to ClickHouse
    write_to_clickhouse(customer_metrics, "customer_sales_report")

def create_time_sales_report():
    """Create time-based sales report"""
    sales_df = read_from_postgres("sales")
    
    # Add time-based columns
    time_sales = sales_df.withColumn("year", year("sale_date")) \
        .withColumn("month", month("sale_date"))
    
    # Calculate metrics
    time_metrics = time_sales.groupBy("year", "month") \
        .agg(
            sum("total_price").alias("monthly_revenue"),
            avg("total_price").alias("avg_order_value"),
            count("*").alias("total_orders")
        )
    
    # Write to ClickHouse
    write_to_clickhouse(time_metrics, "time_sales_report")

def create_store_sales_report():
    """Create store sales report"""
    sales_df = read_from_postgres("sales")
    stores_df = read_from_postgres("stores")
    
    # Join sales with stores
    store_sales = sales_df.join(stores_df, "store_id")
    
    # Calculate metrics
    store_metrics = store_sales.groupBy("store_id", "name", "city", "country") \
        .agg(
            sum("total_price").alias("total_revenue"),
            avg("total_price").alias("avg_order_value"),
            count("*").alias("total_orders")
        )
    
    # Get top 5 stores
    top_stores = store_metrics.orderBy(desc("total_revenue")).limit(5)
    
    # Write to ClickHouse
    write_to_clickhouse(store_metrics, "store_sales_report")

def create_supplier_sales_report():
    """Create supplier sales report"""
    sales_df = read_from_postgres("sales")
    products_df = read_from_postgres("products")
    suppliers_df = read_from_postgres("suppliers")
    
    # Join all tables
    supplier_sales = sales_df.join(products_df, "product_id") \
        .join(suppliers_df, "supplier_id")
    
    # Calculate metrics
    supplier_metrics = supplier_sales.groupBy("supplier_id", "name", "country") \
        .agg(
            sum("total_price").alias("total_revenue"),
            avg("price").alias("avg_product_price"),
            count("*").alias("total_orders")
        )
    
    # Get top 5 suppliers
    top_suppliers = supplier_metrics.orderBy(desc("total_revenue")).limit(5)
    
    # Write to ClickHouse
    write_to_clickhouse(supplier_metrics, "supplier_sales_report")

def create_product_quality_report():
    """Create product quality report"""
    products_df = read_from_postgres("products")
    sales_df = read_from_postgres("sales")
    
    # Join products with sales
    product_quality = products_df.join(sales_df, "product_id", "left")
    
    # Calculate metrics
    quality_metrics = product_quality.groupBy("product_id", "name", "category") \
        .agg(
            avg("rating").alias("avg_rating"),
            sum("reviews").alias("total_reviews"),
            sum("quantity").alias("total_sold"),
            sum("total_price").alias("total_revenue")
        )
    
    # Write to ClickHouse
    write_to_clickhouse(quality_metrics, "product_quality_report")

def main():
    """Main ETL pipeline"""
    print("Starting ETL pipeline...")
    
    # Create all reports
    create_product_sales_report()
    create_customer_sales_report()
    create_time_sales_report()
    create_store_sales_report()
    create_supplier_sales_report()
    create_product_quality_report()
    
    print("ETL pipeline completed successfully!")

if __name__ == "__main__":
    main() 