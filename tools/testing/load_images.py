import requests
import os

# הרשימה מהשלב הקודם (חלק קטן לדוגמה)
items = [
  {"name": "Honey Crisp Apples", "description": "Sweet and crunchy, organic", "price": 4.99, "category": "Fruits", "stock_count": 30},
    {"name": "Almond Milk", "description": "Unsweetened, vanilla flavor", "price": 3.89, "category": "Dairy", "stock_count": 25},
    {"name": "Quinoa", "description": "Organic white quinoa, 1lb", "price": 6.50, "category": "Grains", "stock_count": 18},
    {"name": "Balsamic Vinegar", "description": "Aged, Modena quality", "price": 8.99, "category": "Pantry", "stock_count": 12},
    {"name": "Sourdough Bread", "description": "Artisan loaf, baked fresh", "price": 5.49, "category": "Bakery", "stock_count": 10},
    {"name": "Frozen Blueberries", "description": "Wild caught, no sugar added", "price": 4.25, "category": "Produce", "stock_count": 40},
    {"name": "Ground Beef", "description": "85% lean, grass-fed", "price": 9.99, "category": "Meat & Seafood", "stock_count": 15},
    {"name": "Spinach", "description": "Fresh baby spinach, pre-washed", "price": 3.49, "category": "Produce", "stock_count": 22},
    {"name": "Parmesan Cheese", "description": "Grated, aged 10 months", "price": 6.99, "category": "Dairy", "stock_count": 28},
    {"name": "Sea Salt", "description": "Fine grain, Mediterranean", "price": 2.99, "category": "Pantry", "stock_count": 50},
    {"name": "Chicken Breast", "description": "Boneless, skinless, organic", "price": 11.49, "category": "Meat & Seafood", "stock_count": 14},
    {"name": "Black Beans", "description": "Canned, low sodium", "price": 1.29, "category": "Pantry", "stock_count": 60},
    {"name": "Avocados", "description": "Hass variety, ripe", "price": 1.99, "category": "Produce", "stock_count": 35},
    {"name": "Peanut Butter", "description": "Creamy, all-natural", "price": 4.50, "category": "Pantry", "stock_count": 20},
    {"name": "Oatmeal", "description": "Steel cut, quick cooking", "price": 3.99, "category": "Grains", "stock_count": 32},
    {"name": "Croissants", "description": "Buttery, pack of 4", "price": 6.00, "category": "Bakery", "stock_count": 8},
    {"name": "Cod Fillet", "description": "Wild caught, frozen", "price": 13.99, "category": "Meat & Seafood", "stock_count": 10},
    {"name": "Strawberries", "description": "Fresh local punnet", "price": 5.99, "category": "Fruits", "stock_count": 15},
    {"name": "Soy Milk", "description": "Original, fortified", "price": 3.50, "category": "Dairy", "stock_count": 20},
    {"name": "Red Lentils", "description": "Dried, bulk pack", "price": 2.75, "category": "Grains", "stock_count": 45},
    {"name": "Garlic", "description": "Whole bulbs, organic", "price": 0.99, "category": "Produce", "stock_count": 100},
    {"name": "Mozzarella", "description": "Fresh balls in brine", "price": 5.50, "category": "Dairy", "stock_count": 12},
    {"name": "Pasta", "description": "Penne rigate, semolina", "price": 1.89, "category": "Pantry", "stock_count": 55},
    {"name": "Bagels", "description": "Everything seasoning, 6 pack", "price": 4.99, "category": "Bakery", "stock_count": 15},
    {"name": "Shrimp", "description": "Large, peeled and deveined", "price": 15.99, "category": "Meat & Seafood", "stock_count": 18},
    {"name": "Bananas", "description": "Fair trade, bunch", "price": 1.50, "category": "Fruits", "stock_count": 60}
    # ... שאר 60 הפריטים
]

os.makedirs("product_images", exist_ok=True)

for item in items:
    name = item["name"].replace(" ", "_")
    category = item["category"]
    # פנייה לשירות שמחזיר תמונה לפי קטגוריה/שם
    url = f"https://loremflickr.com/320/240/{category},{name}/all"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"product_images/{name}.png", "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {name}.png")