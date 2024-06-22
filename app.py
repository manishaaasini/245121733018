from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Mock data to simulate the e-commerce APIs responses
mock_data = {
    "AMZ": {
        "Laptop": [
            {"productName": "Laptop 1", "price": 2236, "rating": 4.7, "discount": 63, "availability": "yes"},
            {"productName": "Laptop 13", "price": 1244, "rating": 4.5, "discount": 45, "availability": "out-of-stock"},
            # Add more mock data as needed
        ]
    },
    # Add more companies and categories as needed
}

@app.route('/')
def home():
    return "Welcome to the Top Products HTTP Microservice API!", 200

# Route to register the server with e-commerce companies
@app.route('/register', methods=['POST'])
def register():
    # Simulate registration with the companies
    return jsonify({"status": "registered"}), 200

# Route to get top 'n' products within a category and price range
@app.route('/categories/<category>/products', methods=['GET'])
def get_products(category):
    company = request.args.get('company')
    n = int(request.args.get('top', 10))
    min_price = int(request.args.get('minPrice', 0))
    max_price = int(request.args.get('maxPrice', 100000))
    sort_by = request.args.get('sortBy', 'price')
    sort_order = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))

    if company not in mock_data or category not in mock_data[company]:
        return jsonify({"error": "Company or category not found"}), 404

    products = mock_data[company][category]
    filtered_products = [p for p in products if min_price <= p['price'] <= max_price]
    sorted_products = sorted(filtered_products, key=lambda x: x[sort_by], reverse=(sort_order == 'desc'))
    
    # Pagination
    start_index = (page - 1) * n
    end_index = start_index + n
    paginated_products = sorted_products[start_index:end_index]

    # Add unique identifier to each product
    for product in paginated_products:
        product['id'] = str(uuid.uuid4())

    return jsonify(paginated_products), 200

# Route to get details of a specific product by id
@app.route('/categories/<category>/products/<product_id>', methods=['GET'])
def get_product_details(category, product_id):
    for company in mock_data:
        for product in mock_data[company].get(category, []):
            if product.get('id') == product_id:
                return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
