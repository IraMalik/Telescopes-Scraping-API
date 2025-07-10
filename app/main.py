from flask import Flask, jsonify, request
from scraper import scrape_design_info, scrape_modern_telescopes

app = Flask(__name__)

def get_all_products():
    return scrape_design_info() + scrape_modern_telescopes()

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Refractor Telescope API",
        "routes": ["/products", "/search?q=<keyword>"]
    })

@app.route("/products", methods=["GET"])
def products():
    return jsonify(get_all_products())

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    min_price = request.args.get("min", "")
    max_price = request.args.get("max", "")

    all_products = get_all_products()

    # Filter by title
    results = [p for p in all_products if query in p["title"].lower()]

    # Optional: Clean ₹ symbol and commas
    def clean_price(p):
        try:
            return int(p["price"].replace("₹", "").replace(",", "").strip())
        except:
            return 0

    # Filter by price range
    if min_price:
        results = [p for p in results if clean_price(p) >= int(min_price)]
    if max_price:
        results = [p for p in results if clean_price(p) <= int(max_price)]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)