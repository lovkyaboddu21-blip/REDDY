from flask import Flask, render_template_string, request, session, redirect, url_for, flash
import uuid
from datetime import datetime
import os
import xml.etree.ElementTree as ET 


app = Flask(__name__)
app.secret_key = 'master_elite_security_2026'
USER_DB = "elite_users.txt"

# --- Admin Stats Tracker ---
STATS = {"completed": 0, "canceled": 0, "total_revenue": 0}

# --- Inventory (32 Curated Items) ---
PRODUCTS = [
    {"id": 1, "name": "Quantum Laptop Pro", "category": "Tech", "price": 95000, "img": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500"},
    {"id": 2, "name": "Studio Headphones", "category": "Tech", "price": 18000, "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"},
    {"id": 3, "name": "Mechanical Keyboard", "category": "Tech", "price": 6500, "img": "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500"},
    {"id": 4, "name": "4K Curved Monitor", "category": "Tech", "price": 35000, "img": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500"},
    {"id": 5, "name": "Gaming Mouse RGB", "category": "Tech", "price": 3200, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmDobwfQRwsRTbyjcqvPRkVhfTdHNA2awISg&s"},
    {"id": 6, "name": "1TB External SSD", "category": "Tech", "price": 12000, "img": "https://images.unsplash.com/photo-1597740985671-2a8a3b80502e?w=500"},
    {"id": 7, "name": "Smart Watch Series X", "category": "Tech", "price": 22000, "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"},
    {"id": 8, "name": "Wireless Charging Pad", "category": "Tech", "price": 1500, "img": "https://ptron.in/cdn/shop/files/B0CTHWF16X.PT06.jpg?v=1709710002"},
    {"id": 9, "name": "Python Masterclass", "category": "Education", "price": 499, "img": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500"},
    {"id": 10, "name": "Web Dev Blueprint", "category": "Education", "price": 799, "img": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500"},
    {"id": 11, "name": "DS & Algo Guide", "category": "Education", "price": 1200, "img": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=500"},
    {"id": 12, "name": "AI Foundations Kit", "category": "Education", "price": 2500, "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500"},
    {"id": 13, "name": "Cybersecurity Manual", "category": "Education", "price": 1800, "img": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=500"},
    {"id": 14, "name": "Smart Tablet Pro", "category": "Education", "price": 45000, "img": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500"},
    {"id": 15, "name": "Study Lamp", "category": "Education", "price": 500, "img": "https://rukminim2.flixcart.com/image/480/640/xif0q/table-lamp/l/9/2/touch-switch-desk-night-study-lamp-for-children-reading-office-original-imah54fazkfmhv2q.jpeg?q=90"},
    {"id": 16, "name": "Noise-Block Earbuds", "category": "Education", "price": 990, "img": "https://sm.pcmag.com/pcmag_me/guide/t/the-best-n/the-best-noise-cancelling-true-wireless-earbuds-for-2024_b82e.jpg"},
    {"id": 17, "name": "Official Hoodie", "category": "Lifestyle", "price": 2999, "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500"},
    {"id": 18, "name": "Coffee Flask", "category": "Lifestyle", "price": 1200, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCaU_I_sZ_iuMAXO5gpxICPKzPGyO5hpMdOg&s"},
    {"id": 19, "name": "Anti-Blue Glasses", "category": "Lifestyle", "price": 850, "img": "https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=500"},
    {"id": 20, "name": "Tech Backpack", "category": "Lifestyle", "price": 4500, "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"},
    {"id": 21, "name": "Desk Mat", "category": "Lifestyle", "price": 1500, "img": "https://www.brandless.co.in/cdn/shop/products/Desk_Mat_Tan_2.jpg?v=1640272907&width=1920"},
    {"id": 22, "name": "Smart Bottle", "category": "Lifestyle", "price": 2200, "img": "https://www.mystore.in/s/62ea2c599d1398fa16dbae0a/6784f2d82b92f4751a82973a/4193-jmtnrl.jpg"},
    {"id": 23, "name": "Cotton Tee-shirt", "category": "Lifestyle", "price": 999, "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500"},
    {"id": 24, "name": "Desk Succulent", "category": "Lifestyle", "price": 450, "img": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=500"},
    {"id": 25, "name": "Standing Desk", "category": "Pro Tools", "price": 55000, "img": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=500"},
    {"id": 26, "name": "HD Web Cam", "category": "Pro Tools", "price": 8500, "img": "https://ausha.co.in/cdn/shop/files/1_a4f1f56c-a816-41be-911d-c1fee443042f.png?v=1737107296"},
    {"id": 27, "name": "Ring Light Studio", "category": "Pro Tools", "price": 4200, "img": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=500"},
    {"id": 28, "name": "Sound Panels", "category": "Pro Tools", "price": 6000, "img": "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=500"},
    {"id": 29, "name": "Monitor Arm", "category": "Pro Tools", "price": 7500, "img": "https://rukminim2.flixcart.com/image/480/640/xif0q/monitor-arm/l/d/c/13-27-dual-monitor-arm-with-laptop-clamp-gadget-wagon-original-imagmu4gfn32hx33.jpeg?q=90"},
    {"id": 30, "name": "USB-C Hub", "category": "Pro Tools", "price": 18000, "img": "https://www.ugreenindia.com/cdn/shop/files/61ZrDcJ4nYL._SL1500.jpg?v=1763832403&width=1517"},
    {"id": 31, "name": "Lav Mic", "category": "Pro Tools", "price": 12500, "img": "https://cartnow.in/cdn/shop/files/PU645B.jpg?crop=center&height=368&v=1736068866&width=461"},
    {"id": 32, "name": "Pro Backdrop", "category": "Pro Tools", "price": 3500, "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkKu0RSJN4ZbCQFzEeNSQQPcHrRzwODowlTA&s"},
]

# --- Footer Information Data ---
INFO_PAGES = {
    "story": {"title": "Our Story", "body": "Elite Store (Est. 2026) was built to empower developers. We curate the best gear for creators, ensuring quality you can trust."},
    "careers": {"title": "Careers", "body": "Join the Elite Team! We are looking for talented developers and designers. Send your CV to careers@elitestore.com."},
    "science": {"title": "The Science of Elite", "body": "Our products are selected based on ergonomic research and technical performance to ensure maximum productivity."},
    "sell": {"title": "Merchant Center", "body": "Start selling on Elite. We offer a global platform for tech merchants to reach millions of creators with premium branding."},
    "fulfillment": {"title": "Fulfillment", "body": "We handle the storage, packing, and shipping so you can focus on building your brand."},
    "branding": {"title": "Elite Branding", "body": "Boost your business with our custom tech branding services and professional store setups."},
    "account": {"title": "Your Account", "body": "Manage your orders, update your shipping addresses, and track your Elite points here."},
    "returns": {"title": "Returns & Returns", "body": "7-day easy returns on all tech and lifestyle products. No questions asked."},
    "help-center": {"title": "Help Center", "body": "Need support? Our 24/7 team is ready to assist with any payment or delivery questions."}
}

class EliteXMLManager:
    def __init__(self, filename):
        self.filename = filename
        self._setup()

    def _setup(self):
        """Creates the XML file with Users and Orders sections if it doesn't exist."""
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            root = ET.Element("EliteDatabase")
            ET.SubElement(root, "Users")
            ET.SubElement(root, "Orders") # Section for addresses
            tree = ET.ElementTree(root)
            tree.write(self.filename, encoding="utf-8", xml_declaration=True)

    def register(self, username, password):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        users = root.find("Users")
        for u in users.findall("User"):
            if u.find("Username").text == username: return False
        user = ET.SubElement(users, "User")
        ET.SubElement(user, "Username").text = username
        ET.SubElement(user, "Password").text = password
        tree.write(self.filename)
        return True

    def login(self, username, password):
        try:
            tree = ET.parse(self.filename)
            for u in tree.getroot().find("Users").findall("User"):
                if u.find("Username").text == username and u.find("Password").text == password:
                    return True
        except: pass
        return False

    def save_order(self, username, address, total):
        """Saves the shipping address and order details to XML."""
        tree = ET.parse(self.filename)
        root = tree.getroot()
        orders = root.find("Orders")
        order = ET.SubElement(orders, "Order")
        ET.SubElement(order, "User").text = username
        ET.SubElement(order, "Address").text = address
        ET.SubElement(order, "Total").text = str(total)
        ET.SubElement(order, "Date").text = datetime.now().strftime('%Y-%m-%d %H:%M')
        tree.write(self.filename)

# Initialize the database object
db = EliteXMLManager("elite_database.xml")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <title>Elite Store</title>
    <style>
        * { font-family: 'Poppins', sans-serif; transition: 0.3s ease; }
        body { background: #fdfdfd; color: #1a1a1a; display: flex; flex-direction: column; min-height: 100vh; }
        .brand { font-size: 1.8rem; font-weight: 700; color: #1a1a1a; text-decoration: none; }
        .brand span { color: #f59e0b; }
        
        /* THEME: SHOPPING STOREFRONT BACKGROUND */
        .auth-wrapper { 
            height: 100vh; display: flex; align-items: center; justify-content: center; 
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600&q=80');
            background-size: cover; background-position: center;
        }
        
        /* SEMI-TRANSPARENT GLASS LOGIN CARD */
        .auth-card { 
            background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(20px); 
            padding: 50px 40px; border-radius: 35px; width: 420px; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.3); 
            border: 1px solid rgba(255,255,255,0.3); 
            color: #fff; 
        }

        .auth-card h2 { text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-weight: 700; letter-spacing: 1px; }

        .drawer { position: fixed; top: 0; right: -550px; width: 550px; height: 100%; background: white; box-shadow: -20px 0 60px rgba(0,0,0,0.1); z-index: 2000; padding: 40px; overflow-y: auto;}
        .drawer.open { right: 0; }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); backdrop-filter: blur(8px); display: none; z-index: 1050; }
        .p-card { border: none; border-radius: 20px; overflow: hidden; background: white; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
        .p-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.08); }
        .p-img { height: 200px; object-fit: cover; }

        .v-card { background: linear-gradient(135deg, #2d3436 0%, #000000 100%); border-radius: 20px; padding: 25px; color: white; margin-bottom: 25px; }
        .v-num { font-size: 1.4rem; letter-spacing: 4px; margin: 15px 0; font-weight: 600; }
        
        footer { background: #232f3e; color: #ddd; padding: 60px 0 30px; margin-top: auto; }
        .f-container { max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; padding: 0 40px; }
        .f-col h6 { color: white; font-weight: 700; margin-bottom: 20px; }
        .f-col a { color: #ccc; text-decoration: none; display: block; margin-bottom: 10px; font-size: 14px; }

        .cat-pill { padding: 10px 25px; border-radius: 50px; background: white; color: #555; text-decoration: none; border: 1px solid #ddd; }
        .cat-pill.active { background: #000; color: #fff; border-color: #000; }
        .step-hidden { display: none; }
        .error-msg { background: rgba(255, 255, 255, 0.9); color: #dc2626; padding: 12px; border-radius: 12px; margin-bottom: 20px; font-size: 14px; border: 1px solid #fecaca; }
    </style>
</head>
<body>

    {% if page == 'login' or page == 'register' %}
    <div class="auth-wrapper">
        <div class="auth-card text-center">
            <h2 class="mb-4">{{ 'JOIN ELITE' if page == 'register' else 'ELITE LOGIN' }}</h2>
            
            {% with messages = get_flashed_messages() %}
              {% if messages %}
                {% for message in messages %}
                  <div class="error-msg fw-bold">{{ message }}</div>
                {% endfor %}
              {% endif %}
            {% endwith %}

            <form method="POST" action="{{ url_for('home') if page == 'login' else url_for('register') }}">
                <input type="text" name="u" class="form-control mb-3 p-3 rounded-pill border-0 shadow-sm" placeholder="Username" required autocomplete="off">
                <input type="password" name="p" class="form-control mb-4 p-3 rounded-pill border-0 shadow-sm" placeholder="Password" required>
                <button type="submit" class="btn btn-warning w-100 py-3 rounded-pill fw-bold shadow text-dark">ENTER STORE</button>
            </form>
            <p class="mt-4 small text-white">
                {% if page == 'login' %}
                Don't have an account? <a href="/register" class="text-warning fw-bold text-decoration-none">Create One</a>
                {% else %}
                Already a member? <a href="/" class="text-warning fw-bold text-decoration-none">Login</a>
                {% endif %}
            </p>
        </div>
    </div>
    {% elif page == 'admin' %}
    <div class="container py-5 text-center">
        <h1 class="fw-bold mb-5">ADMIN DASHBOARD</h1>
        <div class="row g-4 justify-content-center">
            <div class="col-md-3"><div class="card p-4 shadow-sm border-0 rounded-4"><h3>Completed</h3><h2 class="text-success fw-bold">{{ stats.completed }}</h2></div></div>
            <div class="col-md-3"><div class="card p-4 shadow-sm border-0 rounded-4"><h3>Canceled</h3><h2 class="text-danger fw-bold">{{ stats.canceled }}</h2></div></div>
            <div class="col-md-3"><div class="card p-4 shadow-sm border-0 rounded-4"><h3>Revenue</h3><h2 class="text-primary fw-bold">₹{{ "{:,}".format(stats.total_revenue) }}</h2></div></div>
        </div>
        <br><br><a href="/logout" class="btn btn-dark rounded-pill px-5">Sign Out Admin</a>
    </div>
    {% elif page == 'info' %}
    <nav class="navbar navbar-expand-lg bg-white sticky-top shadow-sm py-4">
        <div class="container">
            <a class="brand" href="/"> ELITE <span>STORE.</span></a>
        </div>
    </nav>
    <div class="container py-5">
        <div class="card p-5 border-0 shadow-sm rounded-4">
            <h1 class="fw-bold mb-4">{{ info_title }}</h1>
            <p class="lead">{{ info_body }}</p>
            <hr class="my-5">
            <a href="/" class="btn btn-dark rounded-pill px-5 py-3 fw-bold">Back to Shopping</a>
        </div>
    </div>
    {% else %}
    <div class="overlay" id="overlay" onclick="toggleCart()"></div>

    <nav class="navbar navbar-expand-lg bg-white sticky-top shadow-sm py-4">
        <div class="container">
            <a class="brand" href="/"> ELITE <span>STORE.</span></a>
            <div class="d-flex align-items-center gap-3">
                <span class="small fw-bold">Hello, {{ user }}</span>
                <button class="btn btn-dark rounded-pill px-4 fw-bold shadow-sm" onclick="toggleCart()">CART ({{ cart_count }})</button>
                <a href="/logout" class="btn btn-outline-danger btn-sm rounded-pill">Sign Out</a>
            </div>
        </div>
    </nav>

    <div class="container mt-5 flex-grow-1">
        <div class="d-flex flex-wrap gap-2 mb-5 justify-content-center">
            <a href="/" class="cat-pill {% if not active_cat %}active{% endif %}">All Items</a>
            {% for cat in ["Tech", "Education", "Lifestyle", "Pro Tools"] %}
            <a href="/?category={{ cat }}" class="cat-pill {% if active_cat == cat %}active{% endif %}">{{ cat }}</a>
            {% endfor %}
        </div>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4 mb-5">
            {% for p in products %}
            <div class="col">
                <div class="card p-card">
                    <img src="{{ p.img }}" class="p-img" alt="Product Image">
                    <div class="card-body p-4 d-flex flex-column">
                        <small class="text-warning fw-bold">{{ p.category }}</small>
                        <h6 class="fw-bold my-2">{{ p.name }}</h6>
                        <div class="mt-auto d-flex justify-content-between align-items-center pt-3">
                            <span class="fw-bold text-dark">₹{{ "{:,}".format(p.price) }}</span>
                            <a href="/add/{{ p.id }}" class="btn btn-dark btn-sm rounded-pill px-3">Add to Cart</a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="drawer" id="cartDrawer">
        <div class="d-flex justify-content-between mb-4 align-items-center">
            <h3 class="fw-bold m-0">Your Cart</h3>
            <button class="btn-close" onclick="toggleCart()"></button>
        </div>

        {% if cart_items %}
        <div id="step1">
            <div style="max-height: 45vh; overflow-y: auto;" class="pe-2">
                {% for item in cart_items %}
                <div class="d-flex mb-3 align-items-center p-3 border rounded-4 bg-light">
                    <img src="{{ item.img }}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" class="me-3">
                    <div class="flex-grow-1">
                        <h6 class="mb-0 fw-bold small">{{ item.name }}</h6>
                        <span class="text-muted small">₹{{ "{:,}".format(item.price) }}</span>
                    </div>
                </div>
                {% endfor %}
            </div>
            <div class="mt-4 pt-3 border-top">
                <div class="d-flex justify-content-between h4 fw-bold mb-4"><span>Total:</span> <span class="text-dark">₹{{ "{:,}".format(total) }}</span></div>
                <button class="btn btn-dark w-100 py-3 rounded-pill fw-bold shadow" onclick="showStep(2)">Proceed to Delivery →</button>
            </div>
        </div>

        <div id="step2" class="step-hidden">
             <button class="btn btn-sm text-muted mb-3 fw-bold" onclick="showStep(1)">← Edit Cart</button>
             <h5 class="fw-bold mb-3">Shipping Address</h5>
             <input type="text" id="cust_name" class="form-control mb-3 p-3 rounded-4 bg-light border-0" placeholder="Recipient Name" required>
             <input type="text" id="cust_phone" class="form-control mb-3 p-3 rounded-4 bg-light border-0" placeholder="Mobile Number" required>
             <textarea id="cust_address" class="form-control mb-4 p-3 rounded-4 bg-light border-0" placeholder="Full Address (House, Street, Pincode)" rows="3" required></textarea>
             <button class="btn btn-dark w-100 py-3 rounded-pill fw-bold shadow" onclick="validateAddress()">Next: Payment Step →</button>
        </div>

        <div id="step3" class="step-hidden">
            <button class="btn btn-sm text-muted mb-3 fw-bold" onclick="showStep(2)">← Back to Shipping</button>
            <div class="d-flex gap-2 mb-4">
                <button class="btn btn-outline-dark flex-grow-1 rounded-pill active" onclick="setMode('card')" id="cardSwitch">Card</button>
                <button class="btn btn-outline-dark flex-grow-1 rounded-pill" onclick="setMode('upi')" id="upiSwitch">UPI QR</button>
            </div>

            <div id="card-ui">
                <div class="v-card shadow-lg">
                    <div class="v-num" id="d-num">#### #### #### ####</div>
                    <div class="d-flex justify-content-between align-items-end" style="font-size: 0.8rem; text-transform: uppercase;">
                        <div>HOLDER<br><span class="fw-bold">{{ user }}</span></div>
                        <div>EXPIRE<br><span id="d-exp" class="fw-bold">MM/YY</span></div>
                        <div>CVV<br><span id="d-cvv" class="fw-bold">***</span></div>
                    </div>
                </div>
                <form action="/pay" method="POST" id="mainPayForm">
                    <input type="hidden" name="address" id="hidden_address">
                    <input type="text" class="form-control mb-3 p-3 rounded-4 bg-light border-0" placeholder="16 Digit Card Number" maxlength="16" id="c_num" onkeyup="uCard(this.value, 'd-num')" required>
                    <div class="row g-2 mb-4">
                        <div class="col-6"><input type="text" class="form-control p-3 bg-light border-0 rounded-4" placeholder="MM/YY" maxlength="5" id="c_exp" onkeyup="uCard(this.value, 'd-exp')" required></div>
                        <div class="col-6"><input type="password" class="form-control p-3 bg-light border-0 rounded-4" placeholder="CVV" maxlength="3" id="c_cvv" required></div>
                    </div>
                    <div class="d-grid gap-2">
                        <button type="button" class="btn btn-warning py-3 rounded-pill fw-bold shadow" onclick="checkPay()">Final Checkout</button>
                        <a href="/cancel-order" class="btn btn-link text-muted small text-decoration-none">Discard Order</a>
                    </div>
                </form>
            </div>

            <div id="upi-ui" class="step-hidden text-center">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=ElitePayment" class="mb-4 rounded shadow">
                <form action="/pay" method="POST">
                    <input type="hidden" name="address" id="hidden_address_upi">
                    <button class="btn btn-dark w-100 py-3 rounded-pill fw-bold">Complete UPI Payment</button>
                </form>
            </div>
        </div>
        {% else %}
        <p class="text-muted text-center py-5">Your cart is empty.</p>
        {% endif %}
    </div>

<footer>
    <div class="f-container">
        <div class="f-col">
            <h6>About</h6>
            <a href="/info/story">Our Story</a>
            <a href="/info/careers">Careers</a>
            <a href="/info/science">Science</a>
        </div>
        <div class="f-col">
            <h6>Connect</h6>
            <a href="tel:9256785566" style="color: #f59e0b; font-weight: bold;">📞 9256785566</a>
            <a href="https://x.com/Elite_Store5566" target="_blank">Twitter</a>
            <a href="https://www.instagram.com/sto.re6655/?hl=en" target="_blank">Instagram</a>
        </div>
        <div class="f-col">
            <h6>Merchant</h6>
            <a href="/info/sell">Sell Here</a>
            <a href="/info/fulfillment">Fulfillment</a>
            <a href="/info/branding">Branding</a>
        </div>
        <div class="f-col">
            <h6>Help</h6>
            <a href="/info/account">Account</a>
            <a href="/info/returns">Returns</a>
            <a href="/info/help-center">Help Center</a>
        </div>
    </div>
    <div class="text-center mt-5 pt-4 border-top border-secondary">
        <p class="small text-secondary">© 2026 ELITE STORE. Quality You Can Trust.</p>
    </div>
</footer>
    <script>
        function toggleCart() {
            document.getElementById('cartDrawer').classList.toggle('open');
            let o = document.getElementById('overlay');
            o.style.display = (o.style.display === 'block') ? 'none' : 'block';
        }
        function showStep(s) {
            document.getElementById('step1').classList.toggle('step-hidden', s !== 1);
            document.getElementById('step2').classList.toggle('step-hidden', s !== 2);
            document.getElementById('step3').classList.toggle('step-hidden', s !== 3);
        }
        function validateAddress() {
    const name = document.getElementById('cust_name').value;
    const phone = document.getElementById('cust_phone').value;
    const addr = document.getElementById('cust_address').value;
    
    if(!name || !addr || !phone) { 
        alert("Please fill all shipping details!"); 
        return; 
    }
    
    const full_info = name + " | " + phone + " | " + addr;
    
    // This connects the text boxes to the hidden form inputs
    document.getElementById('hidden_address').value = full_info;
    document.getElementById('hidden_address_upi').value = full_info;
    
    showStep(3);
}
        function setMode(m) {
            document.getElementById('card-ui').classList.toggle('step-hidden', m !== 'card');
            document.getElementById('upi-ui').classList.toggle('step-hidden', m !== 'upi');
            document.getElementById('cardSwitch').classList.toggle('active', m === 'card');
            document.getElementById('upiSwitch').classList.toggle('active', m === 'upi');
        }
        function uCard(v, id) {
            let d = document.getElementById(id);
            if(id === 'd-num') d.innerText = v.match(/.{1,4}/g)?.join(' ') || '#### #### #### ####';
            else d.innerText = v || 'MM/YY';
        }
        function checkPay() {
            if(document.getElementById('c_num').value.length < 16 || !document.getElementById('c_exp').value) {
                alert("Please fill all payment fields!"); return;
            }
            document.getElementById('mainPayForm').submit();
        }
        {% if open_cart %} window.onload = toggleCart; {% endif %}
    </script>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        u, p = request.form['u'], request.form['p']
        if u == 'admin' and p == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin'))
        
        # XML LOGIN CONNECTION
        if db.login(u, p):
            session['user'] = u
            return redirect(url_for('home'))
        else:
            flash("Invalid Login! Check XML records.")
            return render_template_string(HTML_TEMPLATE, page='login')
    # ... (rest of your home route logic)
        flash("Username not found!")
        return render_template_string(HTML_TEMPLATE, page='login')

    if 'user' not in session: return render_template_string(HTML_TEMPLATE, page='login')
    if 'cart' not in session: session['cart'] = []
    cat = request.args.get('category')
    filtered = [p for p in PRODUCTS if p['category'] == cat] if cat else PRODUCTS
    cart_items = [p for p in PRODUCTS if p['id'] in session['cart']]
    return render_template_string(HTML_TEMPLATE, products=filtered, active_cat=cat, cart_items=cart_items, total=sum(p['price'] for p in cart_items), cart_count=len(session['cart']), open_cart=request.args.get('open_cart') == 'true', user=session['user'])

@app.route('/info/<topic>')
def info(topic):
    if 'user' not in session: return redirect(url_for('home'))
    data = INFO_PAGES.get(topic, {"title": "Not Found", "body": "This information is currently being updated."})
    return render_template_string(HTML_TEMPLATE, page='info', info_title=data['title'], info_body=data['body'], user=session['user'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u, p = request.form['u'], request.form['p']
        # XML REGISTER CONNECTION
        if db.register(u, p):
            flash("Account created in XML database!")
            return redirect(url_for('home'))
        else:
            flash("Username already exists in XML!")
    return render_template_string(HTML_TEMPLATE, page='register')

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect(url_for('home'))
    return render_template_string(HTML_TEMPLATE, page='admin', stats=STATS)

@app.route('/add/<int:pid>')
def add(pid):
    cart = session.get('cart', []); cart.append(pid); session['cart'] = cart
    return redirect(url_for('home', open_cart='true'))

@app.route('/cancel-order')
def cancel_order():
    STATS['canceled'] += 1
    session['cart'] = []
    return redirect(url_for('home'))

@app.route('/pay', methods=['POST'])
def pay():
    if 'user' not in session: return redirect(url_for('home'))
    
    # Capture address from the hidden input
    address = request.form.get('address', 'No Address Provided')
    
    cart_items = [p for p in PRODUCTS if p['id'] in session.get('cart', [])]
    total = sum(p['price'] for p in cart_items)
    txn_id = "ELITE-" + str(uuid.uuid4()).upper()[:10]
    date_str = datetime.now().strftime('%d %B %Y')

    # SAVE TO XML - This makes the 'address' working
    db.save_order(session['user'], address, total)
    
    STATS['completed'] += 1
    STATS['total_revenue'] += total
    session['cart'] = []

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Official Receipt - {{ txn }}</title>
        <style>
            body { background: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            .receipt-box { max-width: 600px; margin: 50px auto; background: #fff; padding: 40px; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
            @media print { .no-print { display: none; } .receipt-box { box-shadow: none; margin: 0; width: 100%; } }
        </style>
    </head>
    <body>
        <div class="receipt-box">
            <div class="text-center mb-4">
                <h2 class="fw-bold">ELITE STORE</h2>
                <p class="text-muted">Official Transaction Receipt</p>
            </div>
            <hr>
            <div class="row mb-4">
                <div class="col-6">
                    <p class="mb-0 text-muted">Order ID</p>
                    <p class="fw-bold">{{ txn }}</p>
                </div>
                <div class="col-6 text-end">
                    <p class="mb-0 text-muted">Date</p>
                    <p class="fw-bold">{{ date }}</p>
                </div>
            </div>
            <div class="mb-4 p-3 bg-light rounded">
                <p class="mb-1 fw-bold">Shipping Address:</p>
                <p class="mb-0">{{ address }}</p>
            </div>
            <table class="table table-borderless">
                <thead><tr class="border-bottom"><th>Item</th><th class="text-end">Price</th></tr></thead>
                <tbody>
                    {% for item in items %}
                    <tr><td>{{ item.name }}</td><td class="text-end">₹{{ "{:,}".format(item.price) }}</td></tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="border-top pt-3 d-flex justify-content-between align-items-center">
                <h4 class="fw-bold">TOTAL PAID</h4>
                <h4 class="fw-bold text-success">₹{{ "{:,}".format(total) }}</h4>
            </div>
            <div class="mt-5 d-grid gap-2 no-print">
                <button onclick="window.print()" class="btn btn-success py-3 rounded-pill fw-bold">PRINT BILL / SAVE AS PDF</button>
                <a href="/" class="btn btn-outline-dark py-2 rounded-pill">Back to Store</a>
            </div>
        </div>
    </body>
    </html>
    """, txn=txn_id, date=date_str, items=cart_items, total=total, address=address)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
if __name__ == '__main__':
    if not os.path.exists(USER_DB): open(USER_DB, "w").close()
    app.run(debug=True)