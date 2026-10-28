from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__, static_folder="public/static", static_url_path="/static")

CATEGORIES = [
    {"slug": "sand", "name": "Sand", "icon": "⛰", "description": "Building sand and filling sand for your project."},
    {"slug": "stone", "name": "Stone & Aggregate", "icon": "🪨", "description": "Stone, gravel, and aggregate for concrete and foundations."},
    {"slug": "cement", "name": "Cement", "icon": "▤", "description": "Cement and concrete supplies for every stage of the build."},
    {"slug": "steel", "name": "Steel & Rebar", "icon": "〰", "description": "Reinforcement steel for slabs, columns, and foundations."},
    {"slug": "binding-wire", "name": "Binding Wire", "icon": "⌁", "description": "Tie wire for reinforcement and general construction."},
    {"slug": "quarter-wire", "name": "Quarter Wire", "icon": "◌", "description": "Quarter wire and wire products for building work."},
    {"slug": "lumber", "name": "Lumber", "icon": "▰", "description": "Timber and lumber for framing, formwork, and finishing."},
    {"slug": "doors", "name": "Doors", "icon": "▯", "description": "Interior and exterior doors for new builds and renovations."},
    {"slug": "tools", "name": "Tools", "icon": "⚒", "description": "Hand tools and electrical testing tools for home and job-site work."},
    {"slug": "paint", "name": "Paint", "icon": "◒", "description": "Interior and exterior paint for your finishing projects."},
    {"slug": "blocks", "name": "Blocks", "icon": "▦", "description": "Concrete blocks for walls and building projects."},
    {"slug": "plumbing", "name": "Plumbing Equipment", "icon": "🚰", "description": "Pipes, fittings, and tools for plumbing projects."},
]

PRODUCTS = [
    {"id": 2, "name": "Wheelbarrow", "category": "tools", "photo": "wheelbarrow", "price": 12500, "unit": "each", "tag": "Everyday essential", "description": "Heavy-duty wheelbarrow for moving materials around the site."},
    {"id": 3, "name": "Building Sand", "category": "sand", "photo": "building-sand", "price": 9500, "unit": "per cubic yard", "tag": "Bulk material", "description": "Suitable for general masonry and building work. Confirm grade before ordering."},
    {"id": 4, "name": "Filling Sand", "category": "sand", "photo": "filling-sand", "price": 6500, "unit": "per cubic yard", "tag": "Site preparation", "description": "For filling and levelling applications. Delivery quoted separately."},
    {"id": 5, "name": "3/4-inch Stone", "category": "stone", "photo": "aggregate", "price": 11500, "unit": "per cubic yard", "tag": "Concrete aggregate", "description": "Aggregate for concrete mixes and other construction uses."},
    {"id": 6, "name": "Crusher Run", "category": "stone", "photo": "aggregate", "price": 10500, "unit": "per cubic yard", "tag": "Base material", "description": "Compacted base material for suitable site and driveway applications."},
    {"id": 7, "name": "Portland Cement", "category": "cement", "photo": "cement-bags", "price": 1150, "unit": "per bag", "tag": "Popular", "description": "General-purpose cement. Confirm bag size and availability when ordering."},
    {"id": 8, "name": "High-Tensile Rebar", "category": "steel", "photo": "rebar", "price": 1850, "unit": "per length", "tag": "Reinforcement", "description": "Reinforcement bar; choose the required diameter and length when requesting a quote."},
    {"id": 9, "name": "Galvanized Binding Wire", "category": "binding-wire", "photo": "steel-wire", "price": 3200, "unit": "per coil", "tag": "Steel fixing", "description": "Binding wire for tying reinforcement bars and general site use."},
    {"id": 10, "name": "Quarter Wire Coil", "category": "quarter-wire", "photo": "steel-wire", "price": 2800, "unit": "per coil", "tag": "Wire product", "description": "Quarter wire product. Confirm gauge, coil size, and specification before purchase."},
    {"id": 11, "name": "Construction Lumber 2×4", "category": "lumber", "photo": "lumber", "price": 950, "unit": "per length", "tag": "Framing", "description": "Construction timber for framing and formwork. Price depends on length and grade."},
    {"id": 12, "name": "Plywood Sheet", "category": "lumber", "photo": "plywood", "price": 4200, "unit": "per sheet", "tag": "Formwork & boards", "description": "Sheet material for formwork and general building applications."},
    {"id": 13, "name": "Soldering Gun", "category": "tools", "photo": "soldering-gun", "price": 6500, "unit": "each", "tag": "Electrical tool", "description": "Soldering gun for electrical repairs and workshop projects."},
    {"id": 14, "name": "Digital Multimeter", "category": "tools", "photo": "multimeter", "price": 4500, "unit": "each", "tag": "Testing tool", "description": "Digital multimeter for checking electrical measurements."},
    {"id": 15, "name": "Screwdriver Set", "category": "tools", "photo": "screwdriver-set", "price": 2500, "unit": "per set", "tag": "Hand tool", "description": "Assorted screwdrivers for common repair and installation work."},
    {"id": 16, "name": "Interior Paint", "category": "paint", "photo": "paint-bucket", "price": 5500, "unit": "per gallon", "tag": "Interior finish", "description": "Interior paint. Confirm colour, finish, and availability when ordering."},
    {"id": 17, "name": "Exterior Paint", "category": "paint", "photo": "paint-can", "price": 6500, "unit": "per gallon", "tag": "Exterior finish", "description": "Exterior paint. Confirm colour, finish, and availability when ordering."},
    {"id": 18, "name": "Concrete Block", "category": "blocks", "photo": "concrete-block", "price": 250, "unit": "each", "tag": "Building material", "description": "Concrete block. Confirm dimensions and availability before ordering."},
    {"id": 19, "name": "PVC Pipe", "category": "plumbing", "photo": "pvc-fittings", "price": 900, "unit": "per length", "tag": "Plumbing supply", "description": "PVC pipe. Confirm diameter, length, and pressure rating before ordering."},
    {"id": 20, "name": "PVC Elbow Fitting", "category": "plumbing", "photo": "pvc-fittings", "price": 150, "unit": "each", "tag": "Pipe fitting", "description": "PVC elbow fitting. Confirm pipe size and angle before ordering."},
    {"id": 21, "name": "Pipe Wrench", "category": "plumbing", "photo": "pipe-wrench", "price": 2500, "unit": "each", "tag": "Plumbing tool", "description": "Pipe wrench for plumbing installation and repair work."},
    {"id": 22, "name": "PVC Solvent Cement", "category": "plumbing", "photo": "pvc-fittings", "price": 700, "unit": "per tin", "tag": "Pipe adhesive", "description": "PVC solvent cement for joining compatible pipe and fittings. Follow product instructions."},
    {"id": 23, "name": "Interior Flush Door", "category": "doors", "photo": "wooden-door", "price": 9500, "unit": "each", "tag": "Interior door", "description": "Interior flush door. Confirm size, handing, and finish before ordering."},
    {"id": 24, "name": "Exterior Steel Door", "category": "doors", "photo": "wooden-door", "price": 28500, "unit": "each", "tag": "Exterior door", "description": "Exterior steel door. Confirm size, handing, frame, and hardware requirements before ordering."},
    {"id": 25, "name": "Plywood Door", "category": "doors", "photo": "plywood", "price": 12500, "unit": "each", "tag": "Building supply", "description": "Plywood door for building and renovation projects. Confirm size and finish before ordering."},
]

PRODUCT_PHOTOS = {
    "wheelbarrow": {
        "file": "products/wheelbarrow.jpg",
        "alt": "Construction wheelbarrow",
        "credit": "Ildar Sagdejev (Specious)",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:2008-07-15_Construction_wheelbarrow_at_Duke.jpg",
    },
    "building-sand": {
        "file": "products/building-sand.jpg",
        "alt": "Pile of sand for building",
        "credit": "Johnnybam",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Pile_of_Sand_for_Building_in_Anambra_State.jpg",
    },
    "filling-sand": {
        "file": "products/filling-sand.jpg",
        "alt": "Sand used to fill a building foundation",
        "credit": "Johnnybam",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Foundation_Sand_Filling_in_Awka.jpg",
    },
    "aggregate": {
        "file": "products/aggregate.jpg",
        "alt": "20 millimetre stone aggregate",
        "credit": "Billbeee",
        "license": "CC BY 3.0",
        "source": "https://commons.wikimedia.org/wiki/File:20mm-aggregate.jpg",
    },
    "cement-bags": {
        "file": "products/cement-bags.jpg",
        "alt": "Bags of cement",
        "credit": "Wikimedia Commons contributors",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Cement_Baggies.jpg",
    },
    "rebar": {
        "file": "products/rebar.jpg",
        "alt": "Steel reinforcing bars",
        "credit": "W.carter",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:A_bunch_of_rebar_up_close.jpg",
    },
    "steel-wire": {
        "file": "products/steel-wire.jpg",
        "alt": "Coil of steel wire",
        "credit": "Frank Vincentz",
        "license": "CC BY-SA 3.0",
        "source": "https://commons.wikimedia.org/wiki/File:Steel_wire_02_ies.jpg",
    },
    "lumber": {
        "file": "products/lumber.jpg",
        "alt": "Lumber and wood products",
        "credit": "Forest Service Photography",
        "license": "Public domain",
        "source": "https://commons.wikimedia.org/wiki/File:Forest_Products_Week_(20230919-FS-KM-015).jpg",
    },
    "plywood": {
        "file": "products/plywood.jpg",
        "alt": "Sheet of plywood used in building construction",
        "credit": "U.S. Navy",
        "license": "Public domain",
        "source": "https://commons.wikimedia.org/wiki/File:US_Navy_050319-N-9594C-009_Builder_2nd_Class_Thomas_Hurlburt,_a_Seabee_assigned_to_Naval_Mobile_Construction_Battalion_One_(NMCB-1),_carries_a_sheet_of_plywood_during_construction_of_a_three-room_schoolhouse_in_Gonaives,_Haiti.jpg",
    },
    "soldering-gun": {
        "file": "products/soldering-gun.jpg",
        "alt": "Soldering gun",
        "credit": "Jacek Halicki",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:2023_Lutownica_transformatorowa_Lutola_6B.jpg",
    },
    "multimeter": {
        "file": "products/multimeter.jpg",
        "alt": "Digital multimeter",
        "credit": "Jacek Halicki",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:2017_Cyfrowy_miernik_uniwersalny.jpg",
    },
    "screwdriver-set": {
        "file": "products/screwdriver-set.jpg",
        "alt": "Precision screwdriver set",
        "credit": "Project Kei",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:Electronic_Precision_Screwdriver_Set.jpg",
    },
    "paint-bucket": {
        "file": "products/paint-bucket.jpg",
        "alt": "Paint bucket and brush",
        "credit": "Paul The Writer",
        "license": "CC0",
        "source": "https://commons.wikimedia.org/wiki/File:Paint_bucket_and_brush.jpg",
    },
    "paint-can": {
        "file": "products/paint-can.jpg",
        "alt": "Assorted cans of paint",
        "credit": "RAQUIJO",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:001-_PINTURAS_TITANLUX_-_ESMALTE_BRILLANTE.jpg",
    },
    "concrete-block": {
        "file": "products/concrete-block.jpg",
        "alt": "Building constructed with concrete masonry blocks",
        "credit": "Salil Kumar Mukherjee",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:A_building_constructed_with_Concrete_Masonry_blocks.jpg",
    },
    "pvc-fittings": {
        "file": "products/pvc-fittings.jpg",
        "alt": "PVC plumbing pipes and fittings",
        "credit": "Johnnybam",
        "license": "CC BY-SA 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:PVC_plumbing_fittings_in_Awka.jpg",
    },
    "pipe-wrench": {
        "file": "products/pipe-wrench.jpg",
        "alt": "Pipe wrench",
        "credit": "R. Henrik Nilsson",
        "license": "CC BY 4.0",
        "source": "https://commons.wikimedia.org/wiki/File:1970s_Bahco_141_pipe_wrench_made_in_Sweden.jpg",
    },
    "wooden-door": {
        "file": "products/wooden-door.jpg",
        "alt": "Wooden exterior door on a home",
        "credit": "Russell Lee",
        "license": "Public domain",
        "source": "https://commons.wikimedia.org/wiki/File:Door_and_window_in_a_Spanish-American_home_1a34162v.jpg",
    },
}

@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES, products=PRODUCTS, product_photos=PRODUCT_PHOTOS, whatsapp_number=os.environ.get("BUILDMART_WHATSAPP_NUMBER", ""))

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
