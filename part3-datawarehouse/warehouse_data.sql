
-- FLEXIMART DATA WAREHOUSE DATA POPULATION


USE fleximart_dw;


-- 1. INSERT 30 DATES (January-February 2024)

INSERT INTO dim_date (date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend) VALUES
-- January 2024 (15 days)
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, FALSE),
(20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, FALSE),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, FALSE),
(20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, FALSE),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, FALSE),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, TRUE),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, TRUE),
(20240108, '2024-01-08', 'Monday', 8, 1, 'January', 'Q1', 2024, FALSE),
(20240109, '2024-01-09', 'Tuesday', 9, 1, 'January', 'Q1', 2024, FALSE),
(20240110, '2024-01-10', 'Wednesday', 10, 1, 'January', 'Q1', 2024, FALSE),
(20240111, '2024-01-11', 'Thursday', 11, 1, 'January', 'Q1', 2024, FALSE),
(20240112, '2024-01-12', 'Friday', 12, 1, 'January', 'Q1', 2024, FALSE),
(20240113, '2024-01-13', 'Saturday', 13, 1, 'January', 'Q1', 2024, TRUE),
(20240114, '2024-01-14', 'Sunday', 14, 1, 'January', 'Q1', 2024, TRUE),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, FALSE),

-- February 2024 (15 days)
(20240201, '2024-02-01', 'Thursday', 1, 2, 'February', 'Q1', 2024, FALSE),
(20240202, '2024-02-02', 'Friday', 2, 2, 'February', 'Q1', 2024, FALSE),
(20240203, '2024-02-03', 'Saturday', 3, 2, 'February', 'Q1', 2024, TRUE),
(20240204, '2024-02-04', 'Sunday', 4, 2, 'February', 'Q1', 2024, TRUE),
(20240205, '2024-02-05', 'Monday', 5, 2, 'February', 'Q1', 2024, FALSE),
(20240206, '2024-02-06', 'Tuesday', 6, 2, 'February', 'Q1', 2024, FALSE),
(20240207, '2024-02-07', 'Wednesday', 7, 2, 'February', 'Q1', 2024, FALSE),
(20240208, '2024-02-08', 'Thursday', 8, 2, 'February', 'Q1', 2024, FALSE),
(20240209, '2024-02-09', 'Friday', 9, 2, 'February', 'Q1', 2024, FALSE),
(20240210, '2024-02-10', 'Saturday', 10, 2, 'February', 'Q1', 2024, TRUE),
(20240211, '2024-02-11', 'Sunday', 11, 2, 'February', 'Q1', 2024, TRUE),
(20240212, '2024-02-12', 'Monday', 12, 2, 'February', 'Q1', 2024, FALSE),
(20240213, '2024-02-13', 'Tuesday', 13, 2, 'February', 'Q1', 2024, FALSE),
(20240214, '2024-02-14', 'Wednesday', 14, 2, 'February', 'Q1', 2024, FALSE),
(20240215, '2024-02-15', 'Thursday', 15, 2, 'February', 'Q1', 2024, FALSE);

-- 2. INSERT 15 PRODUCTS (3 Categories: Electronics, Fashion, Groceries)
INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
-- Electronics Category (5 products)
('P001', 'Samsung Galaxy S23', 'Electronics', 'Smartphones', 79999.00),
('P002', 'Apple MacBook Air M2', 'Electronics', 'Laptops', 109999.00),
('P003', 'Sony WH-1000XM5', 'Electronics', 'Headphones', 29990.00),
('P004', 'Dell 27-inch Monitor', 'Electronics', 'Monitors', 24999.00),
('P005', 'Apple iPad Air', 'Electronics', 'Tablets', 54999.00),

-- Fashion Category (5 products)
('P006', 'Levi\'s 501 Jeans', 'Fashion', 'Clothing', 3499.00),
('P007', 'Nike Air Max 270', 'Fashion', 'Footwear', 12995.00),
('P008', 'Adidas Originals T-Shirt', 'Fashion', 'Clothing', 1499.00),
('P009', 'Puma Running Shoes', 'Fashion', 'Footwear', 4999.00),
('P010', 'H&M Formal Shirt', 'Fashion', 'Clothing', 1999.00),

-- Groceries Category (5 products)
('P011', 'Basmati Rice 5kg', 'Groceries', 'Grains', 650.00),
('P012', 'Organic Almonds 500g', 'Groceries', 'Dry Fruits', 899.00),
('P013', 'Honey 500g', 'Groceries', 'Sweeteners', 450.00),
('P014', 'Masoor Dal 1kg', 'Groceries', 'Pulses', 120.00),
('P015', 'Sunflower Oil 1L', 'Groceries', 'Oils', 199.00);

-- 3. INSERT 12 CUSTOMERS (4 Cities: Mumbai, Delhi, Bangalore, Chennai)

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
-- Mumbai Customers (3)
('C001', 'Rahul Sharma', 'Mumbai', 'Maharashtra', 'Premium'),
('C002', 'Priya Patel', 'Mumbai', 'Maharashtra', 'Regular'),
('C003', 'Vikram Singh', 'Mumbai', 'Maharashtra', 'New'),

-- Delhi Customers (3)
('C004', 'Anjali Gupta', 'Delhi', 'Delhi', 'Premium'),
('C005', 'Rajesh Kumar', 'Delhi', 'Delhi', 'Regular'),
('C006', 'Sneha Verma', 'Delhi', 'Delhi', 'Loyalty'),

-- Bangalore Customers (3)
('C007', 'Arjun Reddy', 'Bangalore', 'Karnataka', 'Premium'),
('C008', 'Deepa Nair', 'Bangalore', 'Karnataka', 'Regular'),
('C009', 'Karthik Iyer', 'Bangalore', 'Karnataka', 'New'),

-- Chennai Customers (3)
('C010', 'Lakshmi Krishnan', 'Chennai', 'Tamil Nadu', 'Premium'),
('C011', 'Suresh Pillai', 'Chennai', 'Tamil Nadu', 'Regular'),
('C012', 'Meera Sundaram', 'Chennai', 'Tamil Nadu', 'Loyalty');

-- 4. INSERT 40 SALES TRANSACTIONS

INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
-- Weekday Sales (Lower volume - 20 transactions)
(20240101, 1, 1, 1, 79999.00, 2000.00, 77999.00),  -- Jan 1
(20240102, 2, 2, 1, 109999.00, 0.00, 109999.00),   -- Jan 2
(20240102, 3, 3, 2, 29990.00, 500.00, 59480.00),   -- Jan 2
(20240103, 4, 4, 1, 24999.00, 1000.00, 23999.00),  -- Jan 3
(20240103, 5, 5, 1, 54999.00, 0.00, 54999.00),     -- Jan 3
(20240104, 6, 6, 3, 3499.00, 300.00, 10197.00),    -- Jan 4
(20240104, 7, 7, 1, 12995.00, 500.00, 12495.00),   -- Jan 4
(20240105, 8, 8, 5, 1499.00, 200.00, 7295.00),     -- Jan 5
(20240105, 9, 9, 2, 4999.00, 0.00, 9998.00),       -- Jan 5
(20240108, 10, 10, 1, 1999.00, 100.00, 1899.00),   -- Jan 8
(20240108, 11, 11, 10, 650.00, 50.00, 6450.00),    -- Jan 8
(20240109, 12, 12, 3, 899.00, 0.00, 2697.00),      -- Jan 9
(20240109, 13, 1, 5, 450.00, 25.00, 2225.00),      -- Jan 9
(20240110, 14, 2, 20, 120.00, 10.00, 2380.00),     -- Jan 10
(20240110, 15, 3, 8, 199.00, 20.00, 1552.00),      -- Jan 10
(20240111, 1, 4, 1, 79999.00, 3000.00, 76999.00),  -- Jan 11
(20240111, 3, 5, 1, 29990.00, 0.00, 29990.00),     -- Jan 11
(20240112, 7, 6, 2, 12995.00, 400.00, 25590.00),   -- Jan 12
(20240112, 9, 7, 1, 4999.00, 0.00, 4999.00),       -- Jan 12
(20240115, 2, 8, 1, 109999.00, 5000.00, 104999.00),-- Jan 15

-- Weekend Sales (Higher volume - 20 transactions)
(20240106, 1, 9, 1, 79999.00, 1500.00, 78499.00),  -- Jan 6 (Saturday)
(20240106, 4, 10, 2, 24999.00, 800.00, 49198.00),  -- Jan 6 (Saturday)
(20240106, 6, 11, 4, 3499.00, 200.00, 13796.00),   -- Jan 6 (Saturday)
(20240107, 2, 12, 1, 109999.00, 4000.00, 105999.00),-- Jan 7 (Sunday)
(20240107, 5, 1, 2, 54999.00, 1000.00, 108998.00), -- Jan 7 (Sunday)
(20240107, 8, 2, 8, 1499.00, 300.00, 11692.00),    -- Jan 7 (Sunday)
(20240113, 3, 3, 1, 29990.00, 500.00, 29490.00),   -- Jan 13 (Saturday)
(20240113, 7, 4, 3, 12995.00, 600.00, 38385.00),   -- Jan 13 (Saturday)
(20240113, 11, 5, 15, 650.00, 75.00, 9675.00),     -- Jan 13 (Saturday)
(20240114, 9, 6, 2, 4999.00, 200.00, 9798.00),     -- Jan 14 (Sunday)
(20240114, 12, 7, 5, 899.00, 50.00, 4445.00),      -- Jan 14 (Sunday)
(20240114, 15, 8, 12, 199.00, 30.00, 2368.00),     -- Jan 14 (Sunday)
(20240203, 2, 9, 1, 109999.00, 3000.00, 106999.00),-- Feb 3 (Saturday)
(20240203, 6, 10, 6, 3499.00, 400.00, 20594.00),   -- Feb 3 (Saturday)
(20240203, 10, 11, 4, 1999.00, 150.00, 7846.00),   -- Feb 3 (Saturday)
(20240204, 1, 12, 1, 79999.00, 2500.00, 77499.00), -- Feb 4 (Sunday)
(20240204, 5, 1, 1, 54999.00, 1500.00, 53499.00),  -- Feb 4 (Sunday)
(20240204, 13, 2, 8, 450.00, 40.00, 3560.00),      -- Feb 4 (Sunday)
(20240210, 4, 3, 1, 24999.00, 1200.00, 23799.00),  -- Feb 10 (Saturday)
(20240211, 8, 4, 10, 1499.00, 250.00, 14740.00),   -- Feb 11 (Sunday)
(20240211, 14, 5, 25, 120.00, 15.00, 2965.00);     -- Feb 11 (Sunday)

-- 5. VALIDATION QUERIES

-- Show counts to verify minimum requirements
SELECT 
    'dim_date' AS table_name,
    COUNT(*) AS record_count,
    'Minimum: 30' AS requirement
FROM dim_date
UNION ALL
SELECT 
    'dim_product',
    COUNT(*),
    'Minimum: 15'
FROM dim_product
UNION ALL
SELECT 
    'dim_customer',
    COUNT(*),
    'Minimum: 12'
FROM dim_customer
UNION ALL
SELECT 
    'fact_sales',
    COUNT(*),
    'Minimum: 40'
FROM fact_sales;

-- Show product price range
SELECT 
    'Product Price Range' AS metric,
    CONCAT('₹', MIN(unit_price)) AS min_price,
    CONCAT('₹', MAX(unit_price)) AS max_price,
    '₹100 to ₹100,000' AS requirement
FROM dim_product;

-- Show city distribution
SELECT 
    city,
    COUNT(*) AS customer_count,
    GROUP_CONCAT(customer_segment) AS segments
FROM dim_customer
GROUP BY city
ORDER BY customer_count DESC;

-- Show weekend vs weekday sales pattern
SELECT 
    CASE WHEN d.is_weekend = TRUE THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    COUNT(*) AS transaction_count,
    SUM(f.quantity_sold) AS total_units,
    SUM(f.total_amount) AS total_revenue,
    ROUND(AVG(f.quantity_sold), 2) AS avg_quantity
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.is_weekend;