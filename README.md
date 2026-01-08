# FlexiMart Data Architecture Project

**Student Name:** Sri Vamsika Chinta
**Student ID:** bitsom_ba_25071237
**Email:** chintasri2017@gmail.com
**Date:** 08-01-2026

## Project Overview

This project implements a comprehensive data architecture solution for FlexiMart, a retail company. It consists of three main parts: (1) traditional SQL database with ETL pipeline for operational data, (2) NoSQL MongoDB implementation for product catalog, and (3) data warehouse with star schema for analytical processing. The solution demonstrates modern data engineering practices including data validation, transformation, and business intelligence reporting.

## Repository Structure

```
bitsom_ba_25071237-fleximart-data-architecture/
+-- README.md                           # This file
+-- .gitignore                          # Git ignore rules
+-- data/                               # Raw data files
|   +-- customers_raw.csv
|   +-- products_raw.csv
|   +-- sales_raw.csv
+-- part1-database-etl/                 # Part 1: SQL Database & ETL
|   +-- etl_pipeline.py                 # Main ETL pipeline
|   +-- etl_final.py                    # Final ETL version
|   +-- schema_documentation.md         # Database schema design
|   +-- business_queries.sql            # Business intelligence queries
|   +-- data_quality_report.txt         # Data quality analysis
|   +-- requirements.txt                # Python dependencies
|   +-- final_check.py                  # Data validation script
|   +-- mysql_test.py                   # MySQL connection test
|   +-- verify_mysql.py                 # Database verification
+-- part2-nosql/                        # Part 2: NoSQL MongoDB
|   +-- nosql_analysis.md               # NoSQL vs SQL analysis
|   +-- mongodb_operations.js           # MongoDB operations
|   +-- products_catalog.json           # Product catalog data
+-- part3-datawarehouse/                # Part 3: Data Warehouse
    +-- star_schema_design.md           # Star schema documentation
    +-- warehouse_schema.sql            # Warehouse schema SQL
    +-- warehouse_data.sql              # Data loading SQL
    +-- analytics_queries.sql           # OLAP analytics queries
```

## Technologies Used

- **Python 3.x** with pandas, mysql-connector-python
- **MySQL 8.0** for relational database operations
- **MongoDB 6.0** for NoSQL database operations
- **Git** for version control

## Setup Instructions

### Prerequisites
1. Install Python 3.x
2. Install MySQL 8.0
3. Install MongoDB 6.0
4. Install required Python packages: `pip install pandas mysql-connector-python`

### Database Setup

```bash
# Create databases
mysql -u root -p -e "CREATE DATABASE fleximart;"
mysql -u root -p -e "CREATE DATABASE fleximart_dw;"

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql
```

### MongoDB Setup

```bash
mongosh < part2-nosql/mongodb_operations.js
```

## Key Learnings

Through this project, I gained practical experience in designing and implementing end-to-end data architecture solutions. I learned how to:

1. **Build ETL pipelines** with data quality checks and validation
2. **Understand trade-offs** between SQL and NoSQL databases
3. **Design star schemas** for data warehousing and analytical processing
4. **Implement analytical queries** for business intelligence and reporting
5. **Handle data migration** between different database systems

## Challenges Faced

1. **Data Quality Issues**: Raw data contained duplicates and inconsistent formats. Solved by implementing comprehensive data validation and cleaning steps in the ETL pipeline.
2. **Schema Design Decisions**: Balancing normalization vs denormalization required careful consideration. Solved by documenting design decisions and trade-offs in schema documentation.
3. **Cross-database Operations**: Moving data between different database systems required careful mapping of data types and structures. Solved by creating clear transformation logic and documentation.
