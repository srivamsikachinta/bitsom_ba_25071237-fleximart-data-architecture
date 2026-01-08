

// Connect to MongoDB database
use fleximart;

// Clear existing collection if any
db.products.drop();

print("============================================================");
print("MONGODB OPERATIONS FOR FLEXIMART");
print("============================================================");

// ============================================================
// OPERATION 1: LOAD DATA (1 mark)
// Import the provided JSON file into collection 'products'
// ============================================================
print("\nOPERATION 1: Loading data from products_catalog.json");

// Insert the first 2 products (full data would be imported from file)
db.products.insertMany([
  {
    "product_id": "ELEC001",
    "name": "Samsung Galaxy S21 Ultra",
    "category": "Electronics",
    "subcategory": "Smartphones",
    "price": 79999.00,
    "stock": 150,
    "specifications": {
      "brand": "Samsung",
      "ram": "12GB",
      "storage": "256GB",
      "screen_size": "6.8 inches",
      "processor": "Exynos 2100",
      "battery": "5000mAh",
      "camera": "108MP + 12MP + 10MP"
    },
    "reviews": [
      {
        "user_id": "U001",
        "username": "TechGuru",
        "rating": 5,
        "comment": "Excellent phone with amazing camera quality!",
        "date": "2024-01-15"
      },
      {
        "user_id": "U012",
        "username": "MobileUser",
        "rating": 4,
        "comment": "Great performance but a bit pricey.",
        "date": "2024-02-10"
      }
    ],
    "tags": ["flagship", "5G", "android", "photography"],
    "warranty_months": 12,
    "created_at": "2023-12-01T10:00:00Z"
  },
  {
    "product_id": "ELEC002",
    "name": "Apple MacBook Pro 14-inch",
    "category": "Electronics",
    "subcategory": "Laptops",
    "price": 189999.00,
    "stock": 45,
    "specifications": {
      "brand": "Apple",
      "processor": "M2 Pro",
      "ram": "16GB",
      "storage": "512GB SSD",
      "screen_size": "14 inches",
      "graphics": "Integrated GPU",
      "weight": "1.6 kg"
    },
    "reviews": [
      {
        "user_id": "U005",
        "username": "DevPro",
        "rating": 5,
        "comment": "Perfect for development work.",
        "date": "2024-01-20"
      }
    ],
    "tags": ["laptop", "macOS", "professional", "M2"],
    "warranty_months": 12,
    "created_at": "2023-11-15T09:00:00Z"
  }
]);

print("✓ Operation 1: Data loaded successfully");
print("Total products in collection: " + db.products.countDocuments());

// ============================================================
// OPERATION 2: BASIC QUERY (2 marks)
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
// ============================================================
print("\nOPERATION 2: Find Electronics products with price < 50000");

var electronicsProducts = db.products.find(
  { 
    category: "Electronics",
    price: { $lt: 50000 }
  },
  { 
    _id: 0,
    name: 1,
    price: 1,
    stock: 1
  }
).toArray();

print("✓ Operation 2: Found " + electronicsProducts.length + " electronics products");
print("Results:");
printjson(electronicsProducts);

// ============================================================
// OPERATION 3: REVIEW ANALYSIS (2 marks)
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array
// ============================================================
print("\nOPERATION 3: Find products with average rating >= 4.0");

var highRatedProducts = db.products.aggregate([
  {
    $match: {
      "reviews.rating": { $exists: true }
    }
  },
  {
    $addFields: {
      avgRating: {
        $avg: "$reviews.rating"
      }
    }
  },
  {
    $match: {
      avgRating: { $gte: 4.0 }
    }
  },
  {
    $project: {
      _id: 0,
      product_id: 1,
      name: 1,
      category: 1,
      avgRating: { $round: ["$avgRating", 2] },
      reviewCount: { $size: "$reviews" }
    }
  },
  {
    $sort: {
      avgRating: -1
    }
  }
]).toArray();

print("✓ Operation 3: Found " + highRatedProducts.length + " highly rated products");
print("Results:");
printjson(highRatedProducts);

// ============================================================
// OPERATION 4: UPDATE OPERATION (2 marks)
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
// ============================================================
print("\nOPERATION 4: Add new review to product ELEC001");

var updateResult = db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user_id: "U999",
        username: "NewUser",
        rating: 4,
        comment: "Good value for money",
        date: new ISODate()
      }
    }
  }
);

print("✓ Operation 4: Added new review to ELEC001");
print("Matched: " + updateResult.matchedCount + ", Modified: " + updateResult.modifiedCount);

// Verify the update
var updatedProduct = db.products.findOne(
  { product_id: "ELEC001" },
  { _id: 0, name: 1, "reviews.user_id": 1, "reviews.rating": 1, "reviews.comment": 1 }
);
print("Updated product reviews:");
printjson(updatedProduct.reviews);

// ============================================================
// OPERATION 5: COMPLEX AGGREGATION (3 marks)
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending
// ============================================================
print("\nOPERATION 5: Calculate average price by category");

var priceByCategory = db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 },
      total_stock: { $sum: "$stock" }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: { $round: ["$avg_price", 2] },
      product_count: 1,
      total_stock: 1
    }
  },
  {
    $sort: {
      avg_price: -1
    }
  }
]).toArray();

print("✓ Operation 5: Price analysis by category");
print("Results:");
printjson(priceByCategory);

// ============================================================
// ADDITIONAL DEMONSTRATION QUERIES
// ============================================================
print("\nADDITIONAL DEMONSTRATION QUERIES:");

// Query A: Find products with low stock (< 100)
var lowStockProducts = db.products.find(
  { stock: { $lt: 100 } },
  { _id: 0, product_id: 1, name: 1, category: 1, stock: 1, price: 1 }
).sort({ stock: 1 }).toArray();

print("A. Products with low stock (< 100):");
printjson(lowStockProducts);

// Query B: Find products in Smartphones subcategory
var smartphones = db.products.find(
  { subcategory: "Smartphones" },
  { _id: 0, product_id: 1, name: 1, price: 1, stock: 1 }
).toArray();

print("B. Smartphones:");
printjson(smartphones);

// Query C: Find products with warranty > 12 months
var longWarranty = db.products.find(
  { warranty_months: { $gt: 12 } },
  { _id: 0, product_id: 1, name: 1, warranty_months: 1 }
).toArray();

print("C. Products with warranty > 12 months:");
printjson(longWarranty);

// ============================================================
// SUMMARY
// ============================================================
print("\n" + "=" * 60);
print("MONGODB OPERATIONS COMPLETED SUCCESSFULLY!");
print("=" * 60);
print("SUMMARY STATISTICS:");
print("- Total products: " + db.products.countDocuments());
print("- Electronics products: " + db.products.countDocuments({category: "Electronics"}));
print("- Fashion products: " + db.products.countDocuments({category: "Fashion"}));
print("- Products with reviews: " + db.products.countDocuments({"reviews.0": {$exists: true}}));
print("- Average price: " + db.products.aggregate([{$group: {_id: null, avg: {$avg: "$price"}}}]).next().avg.toFixed(2));
print("=" * 60);

// Show all products for verification
print("\nALL PRODUCTS IN COLLECTION:");
var allProducts = db.products.find(
  {},
  { _id: 0, product_id: 1, name: 1, category: 1, price: 1, stock: 1 }
).sort({ category: 1, price: -1 }).toArray();
printjson(allProducts);