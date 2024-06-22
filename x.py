from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

# API credentials and endpoint
API_BASE_URL = "http://20.244.56.144/test"
REGISTER_URL = "http://20.244.56.144/test/register"
AUTH_URL = "http://20.244.56.144/test/auth"
PRODUCTS_URL = "http://20.244.56.144/test/products"

credentials = {
    "companyName": "goMart",
    "clientID": "5c5c398d-253c-4854-b6d2-3d25e3fd5234",
    "clientSecret": "KyQUHafaevMpeEzL",
    "ownerName": "Manisha Asini",
    "ownerEmail": "245121733018@mvsrec.edu.in",
    "rollNo": "2451-21-733-018"
}

# Register the server
def register_server():
    response = requests.post(REGISTER_URL, json=credentials)
    return response.json()

# Obtain authorization token
def get_auth_token():
    response = requests.post(AUTH_URL, json={
        "clientID": credentials["clientID"],
        "clientSecret": credentials["clientSecret"]
    })
    return response.json()["access_token"]

# Fetch products from the API
def fetch_products(category, company, n, min_price, max_price, sort_by, sort_order, page, token):
    headers = {"Authorization": f"Bearer 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE5MDM1NDU0LCJpYXQiOjE3MTkwMzUxNTQsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjVjNWMzOThkLTI1M2MtNDg1NC1iNmQyLTNkMjVlM2ZkNTIzNCIsInN1YiI6IjI0NTEyMTczMzAxOEBtdnNyZWMuZWR1LmluIn0sImNvbXBhbnlOYW1lIjoiZ29NYXJ0IiwiY2xpZW50SUQiOiI1YzVjMzk4ZC0yNTNjLTQ4NTQtYjZkMi0zZDI1ZTNmZDUyMzQiLCJjbGllbnRTZWNyZXQiOiJLeVFVSGFmYWV2TXBlRXpMIiwib3duZXJOYW1lIjoiTWFuaXNoYSBBc2luaSIsIm93bmVyRW1haWwiOiIyNDUxMjE3MzMwMThAbXZzcmVjLmVkdS5pbiIsInJvbGxObyI6IjI0NTEtMjEtNzMzLTAxOCJ9.x0mW2Tin6z_RMjqEFN721Mr-ZHeFC0MX0nQ1S9bt7qk'"}
    params = {
        "category": category,
        "company": company,
        "top": n,
        "minPrice": min_price,
        "maxPrice": max_price,
        "sortBy": sort_by,
        "sortOrder": sort_order,
        "page": page
    }
    response = requests.get(PRODUCTS_URL, headers=headers, params=params)
    return response.json()

@app.route('/')
def home():
    return "Welcome to the Top Products HTTP Microservice API!", 200

@app.route('/register', methods=['POST'])
def register():
    registration_response = register_server()
    return jsonify(registration_response), 200

@app.route('/categories/<category>/products', methods=['GET'])
def get_products(category):
    company = request.args.get('company')
    n = int(request.args.get('top', 10))
    min_price = int(request.args.get('minPrice', 0))
    max_price = int(request.args.get('maxPrice', 100000))
    sort_by = request.args.get('sortBy', 'price')
    sort_order = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))

    token = get_auth_token()

    products_response = fetch_products(
        category=category,
        company=company,
        n=n,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        token=token
    )

    # Add unique identifier to each product
    for product in products_response:
        product['id'] = str(uuid.uuid4())

    return jsonify(products_response), 200

@app.route('/categories/<category>/products/top10amzlaptops', methods=['GET'])
def get_top_10_amz_laptops(category):
    token = get_auth_token()

    # Fetch top 10 AMZ laptops within the price range of 1 to 100000
    products_response = fetch_products(
        category=category,
        company="AMZ",
        n=10,
        min_price=1,
        max_price=100000,
        sort_by="price",
        sort_order="asc",
        page=1,
        token=token
    )

    # Add unique identifier to each product
    for product in products_response:
        product['id'] = str(uuid.uuid4())

    return jsonify(products_response), 200

@app.route('/categories/<category>/products/<product_id>', methods=['GET'])
def get_product_details(category, product_id):
    token = get_auth_token()
    headers = {"Authorization": f"Bearer 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE5MDM1NDU0LCJpYXQiOjE3MTkwMzUxNTQsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjVjNWMzOThkLTI1M2MtNDg1NC1iNmQyLTNkMjVlM2ZkNTIzNCIsInN1YiI6IjI0NTEyMTczMzAxOEBtdnNyZWMuZWR1LmluIn0sImNvbXBhbnlOYW1lIjoiZ29NYXJ0IiwiY2xpZW50SUQiOiI1YzVjMzk4ZC0yNTNjLTQ4NTQtYjZkMi0zZDI1ZTNmZDUyMzQiLCJjbGllbnRTZWNyZXQiOiJLeVFVSGFmYWV2TXBlRXpMIiwib3duZXJOYW1lIjoiTWFuaXNoYSBBc2luaSIsIm93bmVyRW1haWwiOiIyNDUxMjE3MzMwMThAbXZzcmVjLmVkdS5pbiIsInJvbGxObyI6IjI0NTEtMjEtNzMzLTAxOCJ9.x0mW2Tin6z_RMjqEFN721Mr-ZHeFC0MX0nQ1S9bt7qk'"}
    response = requests.get("http://20.244.56.144/test/products/01", headers=headers)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
