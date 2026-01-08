NoSQL Database Analysis - FlexiMart



**Section A:**

**Limitations of RDBMS (150 words)**

**Products with Different Attributes**: RDBMS requires fixed schemas, forcing all products into uniform tables. Laptops (RAM/processor) and shoes (size/color) either create sparse tables with many NULL values or require complex Entity-Attribute-Value patterns, both harming performance and query simplicity.



**Frequent Schema Changes**: Each new product type demands ALTER TABLE operations, causing database downtime and complex migrations. This rigid evolution disrupts agile product catalog expansion, requiring coordinated application updates and risking data inconsistency.



**Nested Customer Reviews**: Reviews with hierarchical comments/replies need multiple normalized tables (products→reviews→comments→replies). Retrieving complete review threads requires expensive JOIN operations across tables, reducing performance and increasing query complexity for nested data naturally suited to document structures.



RDBMS struggles with heterogeneous data models, making flexible product catalogs inefficient and maintenance-heavy.



**Section B:**

**MongoDB Benefits (150 words)**

**Flexible Document Structure:** Each product stores unique attributes naturally as key-value pairs within documents. Laptops include technical specs while shoes contain sizing data, all in the same collection without NULLs or complex joins. Dynamic schema allows instant addition of new product types.



**Embedded Documents**: Customer reviews with nested comments embed directly within product documents, eliminating JOIN operations. Complete review threads retrieve in single reads, improving performance for hierarchical data naturally suited to document models.



**Horizontal Scalability**: MongoDB sharding distributes product data across commodity servers, enabling linear scaling as the catalog grows. Automatic load balancing handles high-volume product searches and concurrent review submissions efficiently.



These features enable rapid catalog evolution, efficient nested data storage, and seamless scaling—critical for expanding e-commerce platforms.



**Section C:** 

**Trade-offs (100 words)**

**1. Transaction Limitations:** MongoDB's document-level atomicity works well within single documents, but complex multi-document transactions (inventory updates across products) are less reliable than MySQL's ACID compliance. Financial operations require careful design.



**2. JOIN Capability Constraints:** While MongoDB provides $lookup for basic joins, it lacks SQL's sophisticated JOIN operations. Complex customer-order-product queries either require denormalization (causing data duplication) or multiple database calls, increasing application complexity and potential inconsistency.



These disadvantages make MongoDB less suitable for transactional systems needing strict consistency, though ideal for flexible product catalogs prioritizing schema evolution over complex transactions.

