CREATE DATABASE IF NOT EXISTS pet_store;

USE pet_store;

-- Product Sales Report
CREATE TABLE IF NOT EXISTS product_sales_report (
    product_id UInt32,
    name String,
    category String,
    total_revenue Decimal(10, 2),
    total_quantity UInt32,
    avg_rating Decimal(3, 2),
    total_reviews UInt32
) ENGINE = MergeTree()
ORDER BY (product_id);

-- Customer Sales Report
CREATE TABLE IF NOT EXISTS customer_sales_report (
    customer_id UInt32,
    first_name String,
    last_name String,
    country String,
    total_spent Decimal(10, 2),
    avg_order_value Decimal(10, 2),
    total_orders UInt32
) ENGINE = MergeTree()
ORDER BY (customer_id);

-- Time Sales Report
CREATE TABLE IF NOT EXISTS time_sales_report (
    year UInt16,
    month UInt8,
    monthly_revenue Decimal(10, 2),
    avg_order_value Decimal(10, 2),
    total_orders UInt32
) ENGINE = MergeTree()
ORDER BY (year, month);

-- Store Sales Report
CREATE TABLE IF NOT EXISTS store_sales_report (
    store_id UInt32,
    name String,
    city String,
    country String,
    total_revenue Decimal(10, 2),
    avg_order_value Decimal(10, 2),
    total_orders UInt32
) ENGINE = MergeTree()
ORDER BY (store_id);

-- Supplier Sales Report
CREATE TABLE IF NOT EXISTS supplier_sales_report (
    supplier_id UInt32,
    name String,
    country String,
    total_revenue Decimal(10, 2),
    avg_product_price Decimal(10, 2),
    total_orders UInt32
) ENGINE = MergeTree()
ORDER BY (supplier_id);

-- Product Quality Report
CREATE TABLE IF NOT EXISTS product_quality_report (
    product_id UInt32,
    name String,
    category String,
    avg_rating Decimal(3, 2),
    total_reviews UInt32,
    total_sold UInt32,
    total_revenue Decimal(10, 2)
) ENGINE = MergeTree()
ORDER BY (product_id); 