from flask import Flask, render_template_string, request, redirect, url_for
import os, csv

app = Flask(__name__)
DB_FILE = "listings.csv"

# Initialize CSV spreadsheet if it does not exist
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Item Name", "Category", "Barangay", "Price", "Contact"])
        writer.writerow(["Hand Tractor (Kubota)", "🔧 Equipment Rental", "Poblacion", "₱1,200 / day", "09171234567"])
        writer.writerow(["Water Pump with Hose", "🔧 Equipment Rental", "Loyonsawang", "₱500 / day", "09229876543"])

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgriShare Abuyog</title>
    <style>
        body { font-family: sans-serif; max-width: 500px; margin: 0 auto; padding: 15px; background: #f4f4f9; color: #333; }
        .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 15px; }
        .price { color: #2e7d32; font-weight: bold; }
        input, select, button { width: 100%; padding: 10px; margin: 5px 0 15px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background: #2e7d32; color: white; font-weight: bold; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h2>🌾 AgriShare Abuyog</h2>
    <p>Hyper-local tool rentals exclusive to Abuyog.</p>
    
    <h3>📋 Active Bulletins</h3>
    {% for row in listings %}
    <div class="card">
        <h4>{{ row[0] }} <small>({{ row[1] }})</small></h4>
        <p>📍 <b>Brgy:</b> {{ row[2] }} | <span class="price">💰 {{ row[3] }}</span></p>
        <p>📞 <b>Contact:</b> <a href="tel:{{ row[4] }}">{{ row[4] }}</a></p>
    </div>
    {% endfor %}

    <h3>➕ Post an Item</h3>
    <form method="POST" action="/add">
        <label>Item Name:</label><input type="text" name="name" required placeholder="e.g., Rice Thresher">
        <label>Category:</label>
        <select name="category">
            <option>🔧 Equipment Rental</option>
            <option>🌱 Input Swap</option>
        </select>
        <label>Barangay:</label><input type="text" name="brgy" required placeholder="e.g., Poblacion">
        <label>Price/Terms:</label><input type="text" name="price" required placeholder="e.g., ₱800 / day">
        <label>Mobile Number:</label><input type="text" name="contact" required placeholder="e.g., 0917XXXXXXX">
        <button type="submit">Publish Bulletin 🚀</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    listings = []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader) # skip header row
        for row in reader:
            listings.append(row)
    return render_template_string(HTML_TEMPLATE, listings=listings)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    category = request.form.get('category')
    brgy = request.form.get('brgy')
    price = request.form.get('price')
    contact = request.form.get('contact')
    
    with open(DB_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, category, brgy, price, contact])
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
