**Star Schema Design Documentation - FlexiMart Data Warehouse**

**Section 1: Schema Overview**

**FACT TABLE: fact\_sales**

Grain: One row per product per order line item (atomic transaction level)

Business Process: Sales transactions analysis



Measures (Numeric Facts):

quantity\_sold: Number of units sold (Integer, NOT NULL)

unit\_price: Price per unit at time of sale (Decimal(10,2), NOT NULL)

discount\_amount: Discount applied to the line item (Decimal(10,2), DEFAULT 0)

total\_amount: Final amount calculated as (quantity × unit\_price - discount) (Decimal(10,2), NOT NULL)

profit\_margin: Calculated profit percentage (Decimal(5,2), NULL)

tax\_amount: Tax applied (Decimal(10,2), DEFAULT 0)



Foreign Keys (Degenerate Dimensions):

date\_key: Integer → Links to dim\_date (Transaction date)

product\_key: Integer → Links to dim\_product

customer\_key: Integer → Links to dim\_customer

order\_id: VARCHAR(20) → Natural key from source system (Degenerate dimension)

transaction\_id: VARCHAR(20) → Unique transaction identifier



Special Attributes:

fact\_sales\_id: Surrogate primary key (BIGINT, AUTO\_INCREMENT)

created\_timestamp: When the record was loaded (TIMESTAMP)

source\_system: Source of the data ('MySQL\_Production')



DIMENSION TABLE: dim\_date

Purpose: Date dimension for comprehensive time-based analysis

Type: Conformed dimension (shared across all facts)

Granularity: Day level



Attributes:

date\_key: Primary key (INTEGER, format: YYYYMMDD, e.g., 20240115)

full\_date: Actual calendar date (DATE, NOT NULL)

day\_of\_week: Integer (1-7, where 1=Monday)

day\_name: Full day name (Monday, Tuesday, etc.)

day\_of\_month: Integer (1-31)

week\_of\_year: Integer (1-52)

month: Integer (1-12)

month\_name: Full month name (January, February, etc.)

quarter: Integer (1-4)

quarter\_name: String (Q1, Q2, Q3, Q4)

year: Integer (e.g., 2023, 2024)

is\_weekend: Boolean (TRUE for Saturday/Sunday)

is\_holiday: Boolean (Indian holidays)

financial\_quarter: String (FY-Q1, FY-Q2, etc.)

financial\_year: Integer (e.g., 2023-24)



DIMENSION TABLE: dim\_product

Purpose: Product master with complete catalog information

Type: Slowly Changing Dimension (Type 2 - maintains history)



Attributes:

product\_key: Surrogate primary key (INTEGER, AUTO\_INCREMENT)

product\_id: Natural business key from source (VARCHAR(20), NOT NULL)

product\_name: Full product name (VARCHAR(100), NOT NULL)

category: Main product category (VARCHAR(50), NOT NULL)

subcategory: Product subcategory (VARCHAR(50))

brand: Manufacturer brand (VARCHAR(50))

price\_range: Category (Budget, Mid-range, Premium)

target\_gender: Target audience (Men, Women, Unisex, Kids)

seasonality: Seasonal classification (All-season, Summer, Winter, Festival)

current\_price: Latest selling price (Decimal(10,2))

cost\_price: Purchase cost (Decimal(10,2), for margin calculation)

supplier\_id: Supplier reference (VARCHAR(20))

date\_added: When product was added to catalog (DATE)

is\_active: Current status (Boolean, DEFAULT TRUE)

valid\_from: SCD Type 2 start date (DATE)

valid\_to: SCD Type 2 end date (DATE, NULL for current)

current\_flag: Indicates current record (Boolean, DEFAULT TRUE)



DIMENSION TABLE: dim\_customer

Purpose: Customer master for demographic analysis

Type: Slowly Changing Dimension (Type 1 - overwrites)



Attributes:

customer\_key: Surrogate primary key (INTEGER, AUTO\_INCREMENT)

customer\_id: Natural business key (VARCHAR(20), NOT NULL)

first\_name: Customer's first name (VARCHAR(50), NOT NULL)

last\_name: Customer's last name (VARCHAR(50), NOT NULL)

full\_name: Concatenated name (VARCHAR(100), NOT NULL)

email: Email address (VARCHAR(100), NOT NULL)

phone: Contact number (VARCHAR(20))

city: City of residence (VARCHAR(50))

state: State (VARCHAR(50))

country: Country (VARCHAR(50), DEFAULT 'India')

customer\_segment: Classification (New, Regular, Premium, Loyalty)

registration\_date: When customer registered (DATE)

age\_group: Demographic grouping (Teen, Young Adult, Adult, Senior)

occupation: Professional category (Student, Professional, Business, etc.)

income\_range: Income bracket (Low, Middle, High, Not Specified)

last\_purchase\_date: Date of most recent purchase (DATE)

total\_orders: Lifetime order count (INTEGER, DEFAULT 0)

total\_spent: Lifetime spending (Decimal(12,2), DEFAULT 0)

customer\_status: Current status (Active, Inactive, Churned)



DIMENSION TABLE: dim\_time (Optional)

Purpose: Time of day analysis for transaction patterns



Attributes:

time\_key: Primary key (INTEGER, format: HHMMSS)

full\_time: Actual time (TIME)

hour: Hour (0-23)

hour\_slot: Classification (Morning: 6-11, Afternoon: 12-17, Evening: 18-23, Night: 0-5)

minute: Minute (0-59)

is\_peak\_hour: Boolean (Based on business hours)

day\_part: String (Early Morning, Morning, Afternoon, Evening, Night)











**Section 2: Design Decisions** 

**Granularity:** Line-item granularity provides maximum analytical flexibility. Each transaction detail is preserved, enabling drilling from yearly totals to individual product sales. This atomic level supports complex what-if analysis, customer behavior tracking, and inventory optimization while allowing aggregation to any level.



**Surrogate Keys:** Implemented for performance and stability. Integer keys enable faster JOINs than VARCHAR natural keys. They're immune to source system changes (product/customer ID changes). Surrogate keys facilitate Type 2 SCD for historical tracking when products or customers change attributes. They handle missing/invalid source keys gracefully, maintaining data warehouse integrity.



**Analytical Support:** Star schema inherently enables OLAP operations. Roll-up aggregates daily→monthly→quarterly sales. Drill-down decomposes category→product→variant performance. Drill-across compares dimensions (products vs customers vs time). Conformed dimensions ensure consistent calculations. Pre-aggregated columns (total\_orders, total\_spent) accelerate common queries while maintaining detailed transaction history for ad-hoc analysis.





**section 3: Sample Data Flow (3 marks)**

**Showing Complete Data Flow**

1\. CREATE TABLES (Star Schema)

Create Star Schema Tables

CREATE DATABASE IF NOT EXISTS fleximart\_dwh;

USE fleximart\_dwh;



&nbsp;--Dimension Table: dim\_date

CREATE TABLE dim\_date (

&nbsp;   date\_key INT PRIMARY KEY,

&nbsp;   full\_date DATE NOT NULL,

&nbsp;   day\_of\_week INT,

&nbsp;   day\_name VARCHAR(10),

&nbsp;   month INT,

&nbsp;   month\_name VARCHAR(10),

&nbsp;   quarter VARCHAR(2),

&nbsp;   year INT,

&nbsp;   is\_weekend BOOLEAN

);



-- Dimension Table: dim\_product

CREATE TABLE dim\_product (

&nbsp;   product\_key INT AUTO\_INCREMENT PRIMARY KEY,

&nbsp;   product\_name VARCHAR(100) NOT NULL,

&nbsp;   category VARCHAR(50),

&nbsp;   brand VARCHAR(50),

&nbsp;   current\_price DECIMAL(10,2)

);



-- Dimension Table: dim\_customer

CREATE TABLE dim\_customer (

&nbsp;   customer\_key INT AUTO\_INCREMENT PRIMARY KEY,

&nbsp;   customer\_name VARCHAR(100) NOT NULL,

&nbsp;   city VARCHAR(50),

&nbsp;   customer\_segment VARCHAR(50)

);



-- Fact Table: fact\_sales

CREATE TABLE fact\_sales (

&nbsp;   date\_key INT NOT NULL,

&nbsp;   product\_key INT NOT NULL,

&nbsp;   customer\_key INT NOT NULL,

&nbsp;   quantity\_sold INT NOT NULL,

&nbsp;   unit\_price DECIMAL(10,2) NOT NULL,

&nbsp;   total\_amount DECIMAL(10,2) NOT NULL,

&nbsp;   FOREIGN KEY (date\_key) REFERENCES dim\_date(date\_key),

&nbsp;   FOREIGN KEY (product\_key) REFERENCES dim\_product(product\_key),

&nbsp;   FOREIGN KEY (customer\_key) REFERENCES dim\_customer(customer\_key)

);

2\. SAMPLE DATA FLOW - STEP BY STEP



-- STEP 1: SOURCE TRANSACTION (Operational DB)

-- Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000

-- This exists in operational database (MySQL - fleximart)



-- STEP 2: LOAD DIMENSIONS (ETL Process)



-- Load dim\_date (Date: 2024-01-15)

INSERT INTO dim\_date (date\_key, full\_date, day\_of\_week, day\_name, month, month\_name, quarter, year, is\_weekend)

VALUES (

&nbsp;   20240115,           -- date\_key (YYYYMMDD format)

&nbsp;   '2024-01-15',       -- full\_date

&nbsp;   2,                  -- day\_of\_week (Monday=1, Tuesday=2)

&nbsp;   'Monday',           -- day\_name

&nbsp;   1,                  -- month

&nbsp;   'January',          -- month\_name

&nbsp;   'Q1',               -- quarter

&nbsp;   2024,               -- year

&nbsp;   FALSE               -- is\_weekend (Monday is not weekend)

);



-- Load dim\_product (Product: Laptop)

INSERT INTO dim\_product (product\_name, category, brand, current\_price)

VALUES (

&nbsp;   'MacBook Pro 16-inch',  -- product\_name

&nbsp;   'Electronics',          -- category

&nbsp;   'Apple',                -- brand

&nbsp;   55000.00               -- current\_price

);

-- This generates product\_key: 5 (auto-increment)



-- Load dim\_customer (Customer: John Doe)

INSERT INTO dim\_customer (customer\_name, city, customer\_segment)

VALUES (

&nbsp;   'John Doe',         -- customer\_name

&nbsp;   'Mumbai',           -- city

&nbsp;   'Premium'           -- customer\_segment

);

-- This generates customer\_key: 12 (auto-increment)



-- STEP 3: LOAD FACT TABLE (ETL Process)



INSERT INTO fact\_sales (date\_key, product\_key, customer\_key, quantity\_sold, unit\_price, total\_amount)

VALUES (

&nbsp;   20240115,   -- date\_key (from dim\_date)

&nbsp;   5,          -- product\_key (from dim\_product - MacBook Pro)

&nbsp;   12,         -- customer\_key (from dim\_customer - John Doe)

&nbsp;   2,          -- quantity\_sold (from source)

&nbsp;   50000.00,   -- unit\_price (from source)

&nbsp;   100000.00   -- total\_amount (calculated: 2 \* 50000)

);

3\. VERIFICATION QUERY - See Complete Data Flow

=

-- QUERY TO SHOW COMPLETE DATA FLOW



-- Show Source Transaction

SELECT 'SOURCE TRANSACTION' as Stage,

&nbsp;      'Order #101' as Reference,

&nbsp;      'John Doe' as Customer,

&nbsp;      'Laptop' as Product,

&nbsp;      2 as Quantity,

&nbsp;      50000.00 as Unit\_Price,

&nbsp;      100000.00 as Total\_Amount

UNION ALL



-- Show Dimension Data

SELECT 'DIMENSION: dim\_date' as Stage,

&nbsp;      CONCAT('Key: ', date\_key) as Reference,

&nbsp;      full\_date as Customer,

&nbsp;      month\_name as Product,

&nbsp;      month as Quantity,

&nbsp;      quarter as Unit\_Price,

&nbsp;      CONCAT('Year: ', year) as Total\_Amount

FROM dim\_date WHERE date\_key = 20240115

UNION ALL



SELECT 'DIMENSION: dim\_product' as Stage,

&nbsp;      CONCAT('Key: ', product\_key) as Reference,

&nbsp;      product\_name as Customer,

&nbsp;      category as Product,

&nbsp;      NULL as Quantity,

&nbsp;      current\_price as Unit\_Price,

&nbsp;      brand as Total\_Amount

FROM dim\_product WHERE product\_key = 5

UNION ALL



SELECT 'DIMENSION: dim\_customer' as Stage,

&nbsp;      CONCAT('Key: ', customer\_key) as Reference,

&nbsp;      customer\_name as Customer,

&nbsp;      city as Product,

&nbsp;      NULL as Quantity,

&nbsp;      customer\_segment as Unit\_Price,

&nbsp;      NULL as Total\_Amount

FROM dim\_customer WHERE customer\_key = 12

UNION ALL



-- Show Fact Table Data

SELECT 'FACT: fact\_sales' as Stage,

&nbsp;      CONCAT('Date: ', date\_key) as Reference,

&nbsp;      CONCAT('Product: ', product\_key) as Customer,

&nbsp;      CONCAT('Customer: ', customer\_key) as Product,

&nbsp;      quantity\_sold as Quantity,

&nbsp;      unit\_price as Unit\_Price,

&nbsp;      total\_amount as Total\_Amount

FROM fact\_sales WHERE date\_key = 20240115 AND product\_key = 5 AND customer\_key = 12;

4\. ANALYTICAL QUERY - Using the Loaded Data



-- ANALYTICAL QUERY: Show Complete Star Join

SELECT 

&nbsp;   d.full\_date,

&nbsp;   d.month\_name,

&nbsp;   d.quarter,

&nbsp;   p.product\_name,

&nbsp;   p.category,

&nbsp;   c.customer\_name,

&nbsp;   c.city,

&nbsp;   f.quantity\_sold,

&nbsp;   f.unit\_price,

&nbsp;   f.total\_amount,

&nbsp;   ROUND(f.total\_amount / f.quantity\_sold, 2) as avg\_price\_per\_unit

FROM fact\_sales f

JOIN dim\_date d ON f.date\_key = d.date\_key

JOIN dim\_product p ON f.product\_key = p.product\_key

JOIN dim\_customer c ON f.customer\_key = c.customer\_key

WHERE f.date\_key = 20240115;









