
import pandas as pd
import numpy as np
import re
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import os

print("=" * 70)
print("FLEXIMART ETL PIPELINE WITH MySQL - STARTING")
print("=" * 70)

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'vamsika2005', 
    'database': 'fleximart'
}

# ============================================================================
# 1. READ CSV FILES
# ============================================================================
print("\nSTEP 1: READING CSV FILES...")

try:
    customers = pd.read_csv('../data/customers_raw.csv')
    products = pd.read_csv('../data/products_raw.csv')
    sales = pd.read_csv('../data/sales_raw.csv')
    
    print(f"✓ customers_raw.csv: {len(customers)} records")
    print(f"✓ products_raw.csv: {len(products)} records")
    print(f"✓ sales_raw.csv: {len(sales)} records")
    
except Exception as e:
    print(f"✗ ERROR reading files: {e}")
    exit(1)

# ============================================================================
# 2. INITIALIZE METRICS
# ============================================================================
metrics = {
    'customers': {
        'processed': len(customers),
        'duplicates_removed': 0,
        'missing_values_handled': 0,
        'loaded_successfully': 0
    },
    'products': {
        'processed': len(products),
        'duplicates_removed': 0,
        'missing_values_handled': 0,
        'loaded_successfully': 0
    },
    'sales': {
        'processed': len(sales),
        'duplicates_removed': 0,
        'missing_values_handled': 0,
        'loaded_successfully': 0
    }
}

# ============================================================================
# 3. CLEAN CUSTOMERS DATA
# ============================================================================
print("\nSTEP 2: CLEANING CUSTOMERS DATA...")

customers_clean = customers.copy()

# Remove duplicates
customers_clean = customers_clean.drop_duplicates(subset=['email'], keep='first')
metrics['customers']['duplicates_removed'] = len(customers) - len(customers_clean)
print(f"✓ Removed {metrics['customers']['duplicates_removed']} duplicate customers")

# Handle missing emails
missing_emails = customers_clean['email'].isna().sum()
if missing_emails > 0:
    for i in range(missing_emails):
        customers_clean.loc[customers_clean['email'].isna(), 'email'] = f"customer_{i+1}@fleximart.com"
    metrics['customers']['missing_values_handled'] += missing_emails
    print(f"✓ Fixed {missing_emails} missing emails")

# Standardize phone format
def fix_phone(phone):
    if pd.isna(phone):
        return 'NOT_PROVIDED'
    phone_str = str(phone)
    digits = re.sub(r'\D', '', phone_str)
    if len(digits) == 10:
        return f"+91-{digits}"
    return phone_str

customers_clean['phone'] = customers_clean['phone'].apply(fix_phone)
print("✓ Standardized phone formats")

# Fix date format
def fix_date(date_str):
    if pd.isna(date_str):
        return datetime.now().strftime('%Y-%m-%d')
    date_str = str(date_str)
    for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except:
            continue
    return datetime.now().strftime('%Y-%m-%d')

customers_clean['registration_date'] = customers_clean['registration_date'].apply(fix_date)
print("✓ Standardized registration dates")

# Fill other missing values
customers_clean['first_name'] = customers_clean['first_name'].fillna('Unknown')
customers_clean['last_name'] = customers_clean['last_name'].fillna('Customer')
customers_clean['city'] = customers_clean['city'].fillna('Unknown')

print(f"✓ Cleaned customers: {len(customers_clean)} records")

# ============================================================================
# 4. CLEAN PRODUCTS DATA
# ============================================================================
print("\nSTEP 3: CLEANING PRODUCTS DATA...")

products_clean = products.copy()

# Remove duplicates
products_clean = products_clean.drop_duplicates(subset=['product_name'], keep='first')
metrics['products']['duplicates_removed'] = len(products) - len(products_clean)
print(f"✓ Removed {metrics['products']['duplicates_removed']} duplicate products")

# Standardize category names
def fix_category(cat):
    if pd.isna(cat):
        return 'Uncategorized'
    cat_lower = str(cat).lower().strip()
    if 'electron' in cat_lower:
        return 'Electronics'
    elif 'fashion' in cat_lower:
        return 'Fashion'
    elif 'home' in cat_lower:
        return 'Home'
    elif 'book' in cat_lower:
        return 'Books'
    elif 'sport' in cat_lower:
        return 'Sports'
    else:
        return cat.title()

products_clean['category'] = products_clean['category'].apply(fix_category)
print("✓ Standardized category names")

# Handle missing prices
missing_prices = products_clean['price'].isna().sum()
if missing_prices > 0:
    products_clean['price'] = products_clean['price'].fillna(0)
    metrics['products']['missing_values_handled'] += missing_prices
    print(f"✓ Fixed {missing_prices} missing prices")

# Handle missing stock
missing_stock = products_clean['stock_quantity'].isna().sum()
if missing_stock > 0:
    products_clean['stock_quantity'] = products_clean['stock_quantity'].fillna(0)
    metrics['products']['missing_values_handled'] += missing_stock
    print(f"✓ Fixed {missing_stock} missing stock quantities")

print(f"✓ Cleaned products: {len(products_clean)} records")

# ============================================================================
# 5. CLEAN SALES DATA
# ============================================================================
print("\nSTEP 4: CLEANING SALES DATA...")

sales_clean = sales.copy()

# Remove duplicates
sales_clean = sales_clean.drop_duplicates(subset=['transaction_id'], keep='first')
metrics['sales']['duplicates_removed'] = len(sales) - len(sales_clean)
print(f"✓ Removed {metrics['sales']['duplicates_removed']} duplicate sales")

# Fix transaction_date
sales_clean['transaction_date'] = sales_clean['transaction_date'].apply(fix_date)
print("✓ Standardized transaction dates")

# Extract numeric IDs from strings like "C001", "P001"
def extract_numeric_id(id_str):
    if pd.isna(id_str):
        return 1
    try:
        numbers = re.sub(r'\D', '', str(id_str))
        if numbers:
            return int(numbers)
        return 1
    except:
        return 1

# Handle customer IDs
if sales_clean['customer_id'].dtype == 'object':
    sales_clean['customer_id'] = sales_clean['customer_id'].apply(extract_numeric_id)
    print("✓ Converted customer IDs to numeric")

missing_customer_ids = sales_clean['customer_id'].isna().sum()
if missing_customer_ids > 0:
    sales_clean['customer_id'] = sales_clean['customer_id'].fillna(1)
    metrics['sales']['missing_values_handled'] += missing_customer_ids
    print(f"✓ Fixed {missing_customer_ids} missing customer IDs")

# Handle product IDs
if sales_clean['product_id'].dtype == 'object':
    sales_clean['product_id'] = sales_clean['product_id'].apply(extract_numeric_id)
    print("✓ Converted product IDs to numeric")

missing_product_ids = sales_clean['product_id'].isna().sum()
if missing_product_ids > 0:
    sales_clean['product_id'] = sales_clean['product_id'].fillna(1)
    metrics['sales']['missing_values_handled'] += missing_product_ids
    print(f"✓ Fixed {missing_product_ids} missing product IDs")

# Handle other missing values
sales_clean['quantity'] = sales_clean['quantity'].fillna(1).astype(int)
sales_clean['unit_price'] = sales_clean['unit_price'].fillna(0)
sales_clean['status'] = sales_clean['status'].fillna('Pending')

print(f"✓ Cleaned sales: {len(sales_clean)} records")

# ============================================================================
# 6. MYSQL DATABASE FUNCTIONS
# ============================================================================
def create_database_connection():
    """Create connection to MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("\n✓ Connected to MySQL database")
            return connection
    except Error as e:
        print(f"\n✗ ERROR connecting to MySQL: {e}")
        print("Trying to create database...")
        return None

def create_database_tables(connection):
    """Create database tables"""
    try:
        cursor = connection.cursor()
        
        # Create customers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            city VARCHAR(50),
            registration_date DATE
        )
        """)
        
        # Create products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            stock_quantity INT DEFAULT 0
        )
        """)
        
        # Create orders table (for sales)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
        """)
        
        connection.commit()
        cursor.close()
        print("✓ Database tables created")
        
    except Error as e:
        print(f"✗ ERROR creating tables: {e}")

def load_customers_to_mysql(connection, customers_df):
    """Load customers data into MySQL"""
    try:
        cursor = connection.cursor()
        loaded = 0
        
        for _, row in customers_df.iterrows():
            try:
                sql = """
                INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    str(row['first_name']),
                    str(row['last_name']),
                    str(row['email']),
                    str(row['phone']),
                    str(row['city']),
                    str(row['registration_date'])
                ))
                loaded += 1
            except mysql.connector.IntegrityError:
                # Skip duplicate emails
                continue
            except Error as e:
                print(f"  Warning inserting customer: {e}")
                continue
        
        connection.commit()
        cursor.close()
        metrics['customers']['loaded_successfully'] = loaded
        print(f"✓ Loaded {loaded} customers to MySQL")
        
    except Error as e:
        print(f"✗ ERROR loading customers: {e}")

def load_products_to_mysql(connection, products_df):
    """Load products data into MySQL"""
    try:
        cursor = connection.cursor()
        loaded = 0
        
        for _, row in products_df.iterrows():
            try:
                sql = """
                INSERT INTO products (product_name, category, price, stock_quantity)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    str(row['product_name']),
                    str(row['category']),
                    float(row['price']),
                    int(row['stock_quantity'])
                ))
                loaded += 1
            except mysql.connector.IntegrityError:
                # Skip duplicate products
                continue
            except Error as e:
                print(f"  Warning inserting product: {e}")
                continue
        
        connection.commit()
        cursor.close()
        metrics['products']['loaded_successfully'] = loaded
        print(f"✓ Loaded {loaded} products to MySQL")
        
    except Error as e:
        print(f"✗ ERROR loading products: {e}")

def load_sales_to_mysql(connection, sales_df):
    """Load sales data into MySQL as orders"""
    try:
        cursor = connection.cursor()
        loaded = 0
        
        for _, row in sales_df.iterrows():
            try:
                # Calculate total amount
                total_amount = float(row['quantity']) * float(row['unit_price'])
                
                sql = """
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    int(row['customer_id']),
                    str(row['transaction_date']),
                    total_amount,
                    str(row['status'])
                ))
                loaded += 1
            except Error as e:
                print(f"  Warning inserting order: {e}")
                continue
        
        connection.commit()
        cursor.close()
        metrics['sales']['loaded_successfully'] = loaded
        print(f"✓ Loaded {loaded} sales/orders to MySQL")
        
    except Error as e:
        print(f"✗ ERROR loading sales: {e}")

# ============================================================================
# 7. LOAD DATA TO MYSQL
# ============================================================================
print("\n" + "="*70)
print("STEP 5: LOADING DATA TO MYSQL DATABASE")
print("="*70)

# Try to connect to MySQL
connection = create_database_connection()

if connection:
    # Create tables
    create_database_tables(connection)
    
    # Load data
    load_customers_to_mysql(connection, customers_clean)
    load_products_to_mysql(connection, products_clean)
    load_sales_to_mysql(connection, sales_clean)
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("✓ MySQL connection closed")
else:
    print("⚠ MySQL connection failed. Data will be saved to CSV files only.")
    
    # Save to CSV as fallback
    customers_clean.to_csv('customers_cleaned.csv', index=False)
    products_clean.to_csv('products_cleaned.csv', index=False)
    sales_clean.to_csv('sales_cleaned.csv', index=False)
    
    metrics['customers']['loaded_successfully'] = len(customers_clean)
    metrics['products']['loaded_successfully'] = len(products_clean)
    metrics['sales']['loaded_successfully'] = len(sales_clean)
    
    print("✓ Data saved to CSV files as fallback")

# ============================================================================
# 8. GENERATE DATA QUALITY REPORT
# ============================================================================
print("\n" + "="*70)
print("STEP 6: GENERATING DATA QUALITY REPORT")
print("="*70)

report = f"""
FLEXIMART DATA QUALITY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Database: {'MySQL' if connection else 'CSV (MySQL failed)'}
{'='*60}

CUSTOMERS:
- Records processed: {metrics['customers']['processed']}
- Duplicates removed: {metrics['customers']['duplicates_removed']}
- Missing values handled: {metrics['customers']['missing_values_handled']}
- Records loaded successfully: {metrics['customers']['loaded_successfully']}

PRODUCTS:
- Records processed: {metrics['products']['processed']}
- Duplicates removed: {metrics['products']['duplicates_removed']}
- Missing values handled: {metrics['products']['missing_values_handled']}
- Records loaded successfully: {metrics['products']['loaded_successfully']}

SALES:
- Records processed: {metrics['sales']['processed']}
- Duplicates removed: {metrics['sales']['duplicates_removed']}
- Missing values handled: {metrics['sales']['missing_values_handled']}
- Records loaded successfully: {metrics['sales']['loaded_successfully']}
{'='*60}

SUMMARY:
- Total records processed: {sum(m['processed'] for m in metrics.values())}
- Total duplicates removed: {sum(m['duplicates_removed'] for m in metrics.values())}
- Total missing values handled: {sum(m['missing_values_handled'] for m in metrics.values())}
- Total records loaded successfully: {sum(m['loaded_successfully'] for m in metrics.values())}
{'='*60}
"""

# Save report to file
with open('data_quality_report.txt', 'w') as f:
    f.write(report)

print("✓ Report saved as 'data_quality_report.txt'")

# ============================================================================
# 9. PRINT FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
print("="*70)
print("\nFILES CREATED:")
print("1. data_quality_report.txt (with all required metrics)")
if not connection:
    print("2. customers_cleaned.csv (MySQL fallback)")
    print("3. products_cleaned.csv (MySQL fallback)")
    print("4. sales_cleaned.csv (MySQL fallback)")

print("\nREPORT METRICS:")
print("-"*60)
print(report)
print("="*70)