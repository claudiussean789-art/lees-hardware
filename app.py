from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

CATEGORIES = [
    {"slug": "sand", "name": "Sand", "icon": "⛰", "description": "Building sand and filling sand for your project."},
    {"slug": "stone", "name": "Stone & Aggregate", "icon": "🪨", "description": "Stone, gravel, and aggregate for concrete and foundations."},
    {"slug": "cement", "name": "Cement", "icon": "▤", "description": "Cement and concrete supplies for every stage of the build."},
    {"slug": "steel", "name": "Steel & Rebar", "icon": "〰", "description": "Reinforcement steel for slabs, columns, and foundations."},
    {"slug": "binding-wire", "name": "Binding Wire", "icon": "⌁", "description": "Tie wire for reinforcement and general construction."},
    {"slug": "quarter-wire", "name": "Quarter Wire", "icon": "◌", "description": "Quarter wire and wire products for building work."},
    {"slug": "lumber", "name": "Lumber", "icon": "▰", "description": "Timber and lumber for framing, formwork, and finishing."},
    {"slug": "tools", "name": "Tools", "icon": "⚒", "description": "Hand tools and electrical testing tools for home and job-site work."},
    {"slug": "paint", "name": "Paint", "icon": "◒", "description": "Interior and exterior paint for your finishing projects."},
    {"slug": "blocks", "name": "Blocks", "icon": "▦", "description": "Concrete blocks for walls and building projects."},
    {"slug": "plumbing", "name": "Plumbing Equipment", "icon": "🚰", "description": "Pipes, fittings, and tools for plumbing projects."},
]

PRODUCTS = [
    {"id": 2, "name": "Wheelbarrow", "category": "tools", "price": 12500, "unit": "each", "tag": "Everyday essential", "description": "Heavy-duty wheelbarrow for moving materials around the site."},
    {"id": 3, "name": "Building Sand", "category": "sand", "price": 9500, "unit": "per cubic yard", "tag": "Bulk material", "description": "Suitable for general masonry and building work. Confirm grade before ordering."},
    {"id": 4, "name": "Filling Sand", "category": "sand", "price": 6500, "unit": "per cubic yard", "tag": "Site preparation", "description": "For filling and levelling applications. Delivery quoted separately."},
    {"id": 5, "name": "3/4-inch Stone", "category": "stone", "price": 11500, "unit": "per cubic yard", "tag": "Concrete aggregate", "description": "Aggregate for concrete mixes and other construction uses."},
    {"id": 6, "name": "Crusher Run", "category": "stone", "price": 10500, "unit": "per cubic yard", "tag": "Base material", "description": "Compacted base material for suitable site and driveway applications."},
    {"id": 7, "name": "Portland Cement", "category": "cement", "price": 1150, "unit": "per bag", "tag": "Popular", "description": "General-purpose cement. Confirm bag size and availability when ordering."},
    {"id": 8, "name": "High-Tensile Rebar", "category": "steel", "price": 1850, "unit": "per length", "tag": "Reinforcement", "description": "Reinforcement bar; choose the required diameter and length when requesting a quote."},
    {"id": 9, "name": "Galvanized Binding Wire", "category": "binding-wire", "price": 3200, "unit": "per coil", "tag": "Steel fixing", "description": "Binding wire for tying reinforcement bars and general site use."},
    {"id": 10, "name": "Quarter Wire Coil", "category": "quarter-wire", "price": 2800, "unit": "per coil", "tag": "Wire product", "description": "Quarter wire product. Confirm gauge, coil size, and specification before purchase."},
    {"id": 11, "name": "Construction Lumber 2×4", "category": "lumber", "price": 950, "unit": "per length", "tag": "Framing", "description": "Construction timber for framing and formwork. Price depends on length and grade."},
    {"id": 12, "name": "Plywood Sheet", "category": "lumber", "price": 4200, "unit": "per sheet", "tag": "Formwork & boards", "description": "Sheet material for formwork and general building applications."},
    {"id": 13, "name": "Soldering Gun", "category": "tools", "price": 6500, "unit": "each", "tag": "Electrical tool", "description": "Soldering gun for electrical repairs and workshop projects."},
    {"id": 14, "name": "Digital Multimeter", "category": "tools", "price": 4500, "unit": "each", "tag": "Testing tool", "description": "Digital multimeter for checking electrical measurements."},
    {"id": 15, "name": "Screwdriver Set", "category": "tools", "price": 2500, "unit": "per set", "tag": "Hand tool", "description": "Assorted screwdrivers for common repair and installation work."},
    {"id": 16, "name": "Interior Paint", "category": "paint", "price": 5500, "unit": "per gallon", "tag": "Interior finish", "description": "Interior paint. Confirm colour, finish, and availability when ordering."},
    {"id": 17, "name": "Exterior Paint", "category": "paint", "price": 6500, "unit": "per gallon", "tag": "Exterior finish", "description": "Exterior paint. Confirm colour, finish, and availability when ordering."},
    {"id": 18, "name": "Concrete Block", "category": "blocks", "price": 250, "unit": "each", "tag": "Building material", "description": "Concrete block. Confirm dimensions and availability before ordering."},
    {"id": 19, "name": "PVC Pipe", "category": "plumbing", "price": 900, "unit": "per length", "tag": "Plumbing supply", "description": "PVC pipe. Confirm diameter, length, and pressure rating before ordering."},
    {"id": 20, "name": "PVC Elbow Fitting", "category": "plumbing", "price": 150, "unit": "each", "tag": "Pipe fitting", "description": "PVC elbow fitting. Confirm pipe size and angle before ordering."},
    {"id": 21, "name": "Pipe Wrench", "category": "plumbing", "price": 2500, "unit": "each", "tag": "Plumbing tool", "description": "Pipe wrench for plumbing installation and repair work."},
    {"id": 22, "name": "PVC Solvent Cement", "category": "plumbing", "price": 700, "unit": "per tin", "tag": "Pipe adhesive", "description": "PVC solvent cement for joining compatible pipe and fittings. Follow product instructions."},
]

@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES, products=PRODUCTS, whatsapp_number=os.environ.get("BUILDMART_WHATSAPP_NUMBER", ""))

@app.route("/api/quote", methods=["POST"])
def quote():
    data = request.get_json(silent=True) or {}
    required = ["name", "phone", "items"]
    if not all(data.get(field) for field in required):
        return jsonify({"ok": False, "message": "Please provide your name, phone number, and at least one item."}), 400
    # Demo mode: no email or database is configured. A real deployment should save this request
    # to a database and/or send it to the store's business email/WhatsApp.
    ref = "BM-" + datetime.now().strftime("%y%m%d%H%M%S")
    return jsonify({
        "ok": True,
        "reference": ref,
        "message": "Your quote request has been prepared. Connect this form to your business email, WhatsApp, or order system before accepting live orders."
    })

if __name__ == "__main__":
    app.run(debug=True)
