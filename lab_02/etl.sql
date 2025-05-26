INSERT INTO customers (first_name, last_name, age, email, country, postal_code)
SELECT DISTINCT 
    customer_first_name,
    customer_last_name,
    customer_age,
    customer_email,
    customer_country,
    customer_postal_code
FROM pet_store_data;

INSERT INTO pets (pet_type, pet_name, pet_breed)
SELECT DISTINCT 
    customer_pet_type,
    customer_pet_name,
    customer_pet_breed
FROM pet_store_data;

INSERT INTO sellers (first_name, last_name, email, country, postal_code)
SELECT DISTINCT 
    seller_first_name,
    seller_last_name,
    seller_email,
    seller_country,
    seller_postal_code
FROM pet_store_data;

INSERT INTO stores (name, location, city, state, country, phone, email)
SELECT DISTINCT 
    store_name,
    store_location,
    store_city,
    store_state,
    store_country,
    store_phone,
    store_email
FROM pet_store_data;

INSERT INTO suppliers (name, contact, email, phone, address, city, country)
SELECT DISTINCT 
    supplier_name,
    supplier_contact,
    supplier_email,
    supplier_phone,
    supplier_address,
    supplier_city,
    supplier_country
FROM pet_store_data;

INSERT INTO products (
    supplier_id, name, category, price, quantity, weight, color, 
    size, brand, material, description, rating, reviews, 
    release_date, expiry_date
)
SELECT DISTINCT 
    s.supplier_id,
    t.product_name,
    t.product_category,
    t.product_price,
    t.product_quantity,
    t.product_weight,
    t.product_color,
    t.product_size,
    t.product_brand,
    t.product_material,
    t.product_description,
    t.product_rating,
    t.product_reviews,
    t.product_release_date,
    t.product_expiry_date
FROM pet_store_data t
JOIN suppliers s ON 
    s.name = t.supplier_name AND
    s.email = t.supplier_email;

INSERT INTO sales (
    customer_id, pet_id, seller_id, store_id, product_id,
    sale_date, quantity, total_price
)
SELECT 
    c.customer_id,
    p.pet_id,
    s.seller_id,
    st.store_id,
    pr.product_id,
    t.sale_date,
    t.sale_quantity,
    t.sale_total_price
FROM pet_store_data t
JOIN customers c ON 
    c.first_name = t.customer_first_name AND
    c.last_name = t.customer_last_name AND
    c.email = t.customer_email
JOIN pets p ON 
    p.pet_name = t.customer_pet_name AND
    p.pet_type = t.customer_pet_type
JOIN sellers s ON 
    s.first_name = t.seller_first_name AND
    s.last_name = t.seller_last_name AND
    s.email = t.seller_email
JOIN stores st ON 
    st.name = t.store_name AND
    st.email = t.store_email
JOIN products pr ON 
    pr.name = t.product_name AND
    pr.category = t.product_category;

