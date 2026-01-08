Database Schema Documentation - FlexiMart

1\. Entity-Relationship Description 



&nbsp;ENTITY: customers

Purpose: Stores customer demographic and contact information  

Attributes:

\- customer\_id: Unique identifier for each customer (Primary Key, Auto-increment)

\- first\_name: Customer's first name (Required, Max 50 characters)

\- last\_name`: Customer's last name (Required, Max 50 characters)

\- email: Customer's email address (Required, Unique, Max 100 characters)

\- phone: Customer's contact number (Optional, Max 20 characters)

\- city: Customer's city of residence (Optional, Max 50 characters)

\- registration\_date: Date when customer registered (Date format)



Relationships:

\- One customer can place MANY orders (1:M relationship with orders table)





ENTITY: products

Purpose: Stores product catalog information  

Attributes:

\- product\_id: Unique identifier for each product (Primary Key, Auto-increment)

\- product\_name: Name of the product (Required, Max 100 characters)

\- category: Product category classification (Required, Max 50 characters)

\- price: Selling price of the product (Required, Decimal with 2 decimal places)

\- stock\_quantity: Available inventory quantity (Default: 0)



Relationships:

\- One product can appear in MANY order items (1:M relationship with order\_items table)

\- Each product belongs to ONE category





ENTITY: orders

Purpose: Stores order transaction information  

Attributes:

\- order\_id: Unique identifier for each order (Primary Key, Auto-increment)

\- customer\_id: Reference to customer who placed the order (Foreign Key to customers table)

\- order\_date: Date when order was placed (Required, Date format)

\- total\_amount: Grand total of the order (Required, Decimal with 2 decimal places)

\- status: Current status of the order (Default: 'Pending', Max 20 characters)



Relationships:

\- Each order belongs to ONE customer (M:1 relationship with customers table)

\- One order can contain MANY order items (1:M relationship with order\_items table)







ENTITY: order\_items

Purpose:Stores individual items within each order (Line items)  

Attributes:

\- order\_item\_id: Unique identifier for each order line item (Primary Key, Auto-increment)

\- order\_id: Reference to the parent order (Foreign Key to orders table)

\- product\_id: Reference to the ordered product (Foreign Key to products table)

\- quantity: Number of units ordered (Required, Integer)

\- unit\_price: Price per unit at time of order (Required, Decimal with 2 decimal places)

\- subtotal: Calculated total for this line item (quantity × unit\_price)



Relationships:

\- Each order item belongs to ONE order (M:1 relationship with orders table)

\- Each order item references ONE product (M:1 relationship with products table)





&nbsp;2. Normalization Explanation (Third Normal Form - 3NF)



Functional Dependencies Identified:



1\. customers table

&nbsp;  - customer\_id → first\_name, last\_name, email,phone, city, registration\_date

&nbsp;  - email → customer\_id (via unique constraint)



2\. products table

&nbsp;  - product\_id → product\_name, category, price, stock\_quantity



3\. orders table:

&nbsp;  - order\_id → customer\_id, order\_date, total\_amount,status

&nbsp;  - customer\_id → (references customers table, not transitive)



4\. order\_items table:

&nbsp;  - order\_item\_id → order\_i, product\_id, quantity, unit\_price, subtotal

&nbsp;  - subtotal = quantity × unit\_price (derived attribute)



&nbsp;Why This Design is in 3NF:



First Normal Form (1NF): All tables satisfy 1NF requirements:

\- Each table has a primary key

\- All column values are atomic (no repeating groups)

\- Each column contains single values

\- Column order doesn't matter



Second Normal Form (2NF): All tables satisfy 2NF requirements:

\- Already in 1NF

\- All non-key attributes are fully functionally dependent on the entire primary key

\- In order\_items, all attributes depend on the composite key (order\_item\_id)



Third Normal Form (3NF): All tables satisfy 3NF requirements:

\- Already in 2NF

\- No transitive dependencies exist (non-key attributes don't depend on other non-key attributes)

\- All non-key attributes depend only on the primary key



&nbsp;How the Design Avoids Anomalies:



Update Anomalies Avoided:

\- Customer information is stored only in the `customers` table. If a customer updates their phone number, it needs to be changed in only one place.

\- Product details are centralized in the `products` table, preventing inconsistent product information across orders.



Insert Anomalies Avoided:

\- New products can be added to the `products` table without requiring any orders.

\- New customers can register without placing orders.

\- The separation of `orders` and `order\_items` allows creating order headers before adding line items.



Delete Anomalies Avoided:

\- Deleting an order doesn't delete customer information (customer remains in the database).

\- Removing a product from catalog doesn't affect historical order records (order\_items preserve the product details as they were at order time).

\- The referential integrity with foreign keys ensures data consistency during deletions.



The schema achieves \*\*3NF\*\* by eliminating all transitive dependencies and ensuring that each table represents a single entity or relationship. The design supports efficient queries while maintaining data integrity through proper foreign key constraints and normalized structure.



---



&nbsp;3. Sample Data Representation



Table: customers

| customer\_id | first\_name | last\_name | email | phone | city | registration\_date |

|------------|------------|-----------|----------------------|----------------|-----------|-------------------|

| 1 | Rahul | Sharma | rahul.sharma@gmail.com | +91-9876543210 | Bangalore | 2023-01-15 |

| 2 | Priya | Patel | priya.patel@yahoo.com | +91-9988776655 | Mumbai | 2023-02-20 |

| 3 | Sneha | Reddy | sneha.reddy@gmail.com | +91-9123456789 | Hyderabad | 2023-04-15 |



Table: products

| product\_id | product\_name | category | price | stock\_quantity |

|------------|--------------|----------|----------|----------------|

| 1 | Samsung Galaxy S21 | Electronics | 45999.00 | 150 |

| 2 | Nike Running Shoes | Fashion | 3499.00 | 80 |

| 3 | Apple MacBook Pro | Electronics | 2999.00 | 45 |



Table: orders

| order\_id | customer\_id | order\_date | total\_amount | status |

|----------|-------------|------------|--------------|---------|

| 1 | 1 | 2024-01-15 | 45999.00 | Completed |

| 2 | 2 | 2024-01-16 | 5998.00 | Completed |

| 3 | 3 | 2024-01-17 | 52999.00 | Completed |



Table: order\_items

| order\_item\_id | order\_id | product\_id | quantity | unit\_price | subtotal |

|---------------|----------|------------|----------|------------|----------|

| 1 | 1 | 1 | 1 | 45999.00 | 45999.00 |

| 2 | 2 | 2 | 2 | 2999.00 | 5998.00 |

| 3 | 3 | 3 | 1 | 52999.00 | 52999.00 |



---



&nbsp;4. Relationships Summary



mermaid

graph LR

&nbsp;   C\[customers] -- 1:M --> O\[orders]

&nbsp;   O -- 1:M --> I\[order\_items]

&nbsp;   P\[products] -- 1:M --> I

&nbsp;   

&nbsp;   C -->|customer\_id| O

&nbsp;   O -->|order\_id| I

&nbsp;   P -->|product\_id| I

