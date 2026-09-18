from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from datetime import datetime
import hashlib
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# ===== TRANSLATIONS =====
translations = {
    'en': {
        'app_name': 'SmartPantry AI',
        'home': 'Home',
        'features': 'Features',
        'recipes': 'Recipes',
        'about': 'About',
        'contact': 'Contact',
        'login': 'Login',
        'signup': 'Sign Up',
        'dashboard': 'Dashboard',
        'logout': 'Logout',
        'hero_title': 'Smart Pantry AI',
        'hero_description': 'Helps you reduce food waste, save money, and eat healthier.',
        'get_started': 'Get Started Free',
        'learn_more': 'Learn More',
        'ai_algorithms': 'AI Algorithms',
        'active_users': 'Active Users',
        'waste_reduction': 'Waste Reduction',
        'features_title': 'Everything You Need to Manage Your Kitchen',
        'features_subtitle': 'Powered by 15+ AI algorithms to make your life easier',
        'how_it_works': 'How It Works',
        'step1_title': 'Add Your Items',
        'step1_desc': 'Log your groceries manually or scan barcodes',
        'step2_title': 'AI Analyzes',
        'step2_desc': 'Our AI tracks usage patterns and predicts needs',
        'step3_title': 'Get Insights',
        'step3_desc': 'Receive smart suggestions and alerts',
        'newsletter': 'Newsletter',
        'subscribe': 'Subscribe',
        'email_placeholder': 'Your email',
        'quick_links': 'Quick Links',
        'support': 'Support',
        'connect': 'Connect',
        'inventory': 'Inventory',
        'expiry_alerts': 'Expiry Alerts',
        'shopping_list': 'Shopping List',
        'recipe_planner': 'Recipe Planner',
        'analytics': 'Analytics',
        'nutrition': 'Nutrition',
        'total_calories': 'Total Calories',
        'protein': 'Protein',
        'carbs': 'Carbs',
        'fat': 'Fat',
        'fiber': 'Fiber',
        'all_rights_reserved': 'All rights reserved.',
        'ai_powered': 'AI-Powered Kitchen Management',
        'simple_intelligent': 'Simple & Intelligent',
        'pantry': 'Pantry',
        'low_stock': 'Low Stock',
        'expiring_soon': 'Expiring Soon',
        'monthly_expense': 'Monthly Expense',
        'usage_forecast': 'Usage (7d forecast)',
        'waste_analysis': 'Waste reduction',
        'budget_tip': 'Buy rice & pasta in bulk to save 15%',
        'apply': 'Apply',
        'predict': 'Predict',
        'refresh': 'Refresh',
        'add_item': 'Add Item',
        'update': 'Update',
        'cancel': 'Cancel',
        'confirm': 'Confirm',
        'item_name': 'Item Name',
        'quantity': 'Quantity',
        'unit': 'Unit',
        'expiry_date': 'Expiry Date',
        'category': 'Category',
        'add_new_item': 'Add New Item',
        'enter_details': 'Enter the details for your new grocery item:',
        'shopping_list_title': 'AI Shopping List',
        'generate_list': 'Generate List',
        'clear_list': 'Clear List',
        'no_items': 'No items in inventory',
        'all_stocked': 'All items are well stocked!',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'invalid_credentials': 'Invalid username or password',
        'username_exists': 'Username already exists',
        'account_created': 'Account created successfully! Please login.',
        'welcome_back': 'Welcome back',
        'inventory_management': 'Inventory Management',
        'recipe_recommendations': 'Recipe Recommendations',
        'budget_tracker': 'Budget Tracker',
        'total_items': 'Total Items',
        'need_restock': 'need restock',
        'days_left': 'days left',
        'items_to_buy': 'Items to buy',
        'recipes_ready': 'Recipes ready',
        'available': 'available'
    },
    'hi': {
        'app_name': 'स्मार्टपैंट्री एआई',
        'home': 'होम',
        'features': 'फीचर्स',
        'recipes': 'रेसिपी',
        'about': 'हमारे बारे में',
        'contact': 'संपर्क करें',
        'login': 'लॉगिन',
        'signup': 'साइन अप',
        'dashboard': 'डैशबोर्ड',
        'logout': 'लॉगआउट',
        'hero_title': 'स्मार्ट पेंट्री एआई',
        'hero_description': 'खाने की बर्बादी कम करने, पैसे बचाने और स्वस्थ खाने में आपकी मदद करता है।',
        'get_started': 'मुफ्त शुरू करें',
        'learn_more': 'और जानें',
        'ai_algorithms': 'एआई एल्गोरिदम',
        'active_users': 'सक्रिय उपयोगकर्ता',
        'waste_reduction': 'बर्बादी में कमी',
        'features_title': 'आपकी रसोई प्रबंधित करने के लिए सब कुछ',
        'features_subtitle': 'आपके जीवन को आसान बनाने के लिए 15+ एआई एल्गोरिदम',
        'how_it_works': 'यह कैसे काम करता है',
        'step1_title': 'अपनी वस्तुएं जोड़ें',
        'step1_desc': 'अपना सामान मैन्युअल रूप से लॉग करें या बारकोड स्कैन करें',
        'step2_title': 'एआई विश्लेषण',
        'step2_desc': 'हमारी एआई उपयोग पैटर्न ट्रैक करती है और जरूरतों की भविष्यवाणी करती है',
        'step3_title': 'जानकारी प्राप्त करें',
        'step3_desc': 'स्मार्ट सुझाव और अलर्ट प्राप्त करें',
        'newsletter': 'न्यूज़लेटर',
        'subscribe': 'सब्सक्राइब करें',
        'email_placeholder': 'आपका ईमेल',
        'quick_links': 'त्वरित लिंक',
        'support': 'सहायता',
        'connect': 'जुड़ें',
        'inventory': 'इन्वेंटरी',
        'expiry_alerts': 'समाप्ति अलर्ट',
        'shopping_list': 'शॉपिंग लिस्ट',
        'recipe_planner': 'रेसिपी प्लानर',
        'analytics': 'एनालिटिक्स',
        'nutrition': 'पोषण',
        'total_calories': 'कुल कैलोरी',
        'protein': 'प्रोटीन',
        'carbs': 'कार्ब्स',
        'fat': 'फैट',
        'fiber': 'फाइबर',
        'all_rights_reserved': 'सभी अधिकार सुरक्षित।',
        'ai_powered': 'एआई-संचालित किचन मैनेजमेंट',
        'simple_intelligent': 'सरल और बुद्धिमान',
        'pantry': 'पेंट्री',
        'low_stock': 'कम स्टॉक',
        'expiring_soon': 'जल्दी समाप्त हो रहा है',
        'monthly_expense': 'मासिक खर्च',
        'usage_forecast': 'उपयोग पूर्वानुमान (7 दिन)',
        'waste_analysis': 'बर्बादी में कमी',
        'budget_tip': 'चावल और पास्ता थोक में खरीदें, 15% बचाएं',
        'apply': 'लागू करें',
        'predict': 'भविष्यवाणी करें',
        'refresh': 'रिफ्रेश करें',
        'add_item': 'आइटम जोड़ें',
        'update': 'अपडेट करें',
        'cancel': 'रद्द करें',
        'confirm': 'पुष्टि करें',
        'item_name': 'आइटम का नाम',
        'quantity': 'मात्रा',
        'unit': 'इकाई',
        'expiry_date': 'समाप्ति तिथि',
        'category': 'श्रेणी',
        'add_new_item': 'नया आइटम जोड़ें',
        'enter_details': 'अपने नए ग्रोसरी आइटम का विवरण दर्ज करें:',
        'shopping_list_title': 'एआई शॉपिंग लिस्ट',
        'generate_list': 'लिस्ट बनाएं',
        'clear_list': 'लिस्ट साफ करें',
        'no_items': 'इन्वेंटरी में कोई आइटम नहीं',
        'all_stocked': 'सभी आइटम अच्छी तरह से स्टॉक हैं!',
        'loading': 'लोड हो रहा है...',
        'error': 'त्रुटि',
        'success': 'सफलता',
        'invalid_credentials': 'अमान्य उपयोगकर्ता नाम या पासवर्ड',
        'username_exists': 'उपयोगकर्ता नाम पहले से मौजूद है',
        'account_created': 'खाता सफलतापूर्वक बनाया गया! कृपया लॉगिन करें।',
        'welcome_back': 'वापसी पर स्वागत है',
        'inventory_management': 'इन्वेंटरी प्रबंधन',
        'recipe_recommendations': 'रेसिपी सुझाव',
        'budget_tracker': 'बजट ट्रैकर',
        'total_items': 'कुल आइटम',
        'need_restock': 'पुनः स्टॉक की आवश्यकता',
        'days_left': 'दिन शेष',
        'items_to_buy': 'खरीदने के लिए आइटम',
        'recipes_ready': 'रेसिपी तैयार',
        'available': 'उपलब्ध'
    }
}

def get_text(key, lang='en'):
    if lang not in translations:
        lang = 'en'
    return translations[lang].get(key, key)

# ===== DATA FILES =====
USERS_FILE = 'data/users.json'
INVENTORY_FILE = 'data/inventory.json'
os.makedirs('data', exist_ok=True)

def init_data_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(INVENTORY_FILE):
        default_inventory = {
            "items": [
                {"id": 1, "name": "Apples", "quantity": 3, "unit": "pcs", "expiry": "2026-09-10", "category": "Fruits"},
                {"id": 2, "name": "Eggs", "quantity": 2, "unit": "pcs", "expiry": "2026-09-12", "category": "Dairy"},
                {"id": 3, "name": "Bread", "quantity": 1, "unit": "loaf", "expiry": "2026-09-08", "category": "Bakery"},
                {"id": 4, "name": "Milk", "quantity": 1, "unit": "L", "expiry": "2026-09-06", "category": "Dairy"},
                {"id": 5, "name": "Cheddar Cheese", "quantity": 1, "unit": "block", "expiry": "2026-09-07", "category": "Dairy"},
                {"id": 6, "name": "Tomatoes", "quantity": 4, "unit": "pcs", "expiry": "2026-09-11", "category": "Vegetables"},
                {"id": 7, "name": "Onions", "quantity": 3, "unit": "pcs", "expiry": "2026-09-15", "category": "Vegetables"},
                {"id": 8, "name": "Chicken Breast", "quantity": 2, "unit": "pcs", "expiry": "2026-09-09", "category": "Meat"}
            ],
            "next_id": 9
        }
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(default_inventory, f)

init_data_files()

# ===== HELPERS =====
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_inventory():
    with open(INVENTORY_FILE, 'r') as f:
        return json.load(f)

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ===== LANGUAGE ROUTE =====
@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in ['en', 'hi']:
        session['language'] = lang
    return redirect(request.referrer or url_for('index'))

# ===== MAIN ROUTES =====
@app.route('/')
def index():
    lang = session.get('language', 'en')
    return render_template('index.html', lang=lang, text=get_text)

@app.route('/features')
def features():
    lang = session.get('language', 'en')
    return render_template('features.html', lang=lang, text=get_text)

@app.route('/about')
def about():
    lang = session.get('language', 'en')
    return render_template('about.html', lang=lang, text=get_text)

@app.route('/contact')
def contact():
    lang = session.get('language', 'en')
    return render_template('contact.html', lang=lang, text=get_text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('language', 'en')
    if request.method == 'POST':
        username = request.form.get('username')
        password = hash_password(request.form.get('password'))
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=get_text('invalid_credentials', lang), lang=lang, text=get_text)
    return render_template('login.html', lang=lang, text=get_text)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    lang = session.get('language', 'en')
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = hash_password(request.form.get('password'))
        users = load_users()
        if username in users:
            return render_template('signup.html', error=get_text('username_exists', lang), lang=lang, text=get_text)
        users[username] = {
            'id': len(users) + 1,
            'username': username,
            'email': email,
            'password': password,
            'created_at': datetime.now().isoformat()
        }
        save_users(users)
        return redirect(url_for('login', message=get_text('account_created', lang)))
    return render_template('signup.html', lang=lang, text=get_text)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    user = users.get(session['username'], {})
    inventory = load_inventory()
    
    # Count stats
    total_items = len(inventory['items'])
    total_categories = len(set(item['category'] for item in inventory['items']))
    
    return render_template('profile.html',
                         username=session['username'],
                         user=user,
                         total_items=total_items,
                         total_categories=total_categories)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    lang = session.get('language', 'en')
    inventory = load_inventory()
    items = inventory['items']
    total_items = len(items)
    low_stock = [item for item in items if item['quantity'] <= 2]
    today = datetime.now().date()
    expiring = []
    for item in items:
        try:
            expiry_date = datetime.strptime(item['expiry'], '%Y-%m-%d').date()
            days_left = (expiry_date - today).days
            if 0 <= days_left <= 3:
                expiring.append({**item, 'days_left': days_left})
        except:
            pass
    return render_template('dashboard.html',
                         username=session['username'],
                         items=items,
                         total_items=total_items,
                         low_stock=low_stock,
                         expiring=expiring,
                         lang=lang,
                         text=get_text)

# ===== INVENTORY PAGE =====
@app.route('/inventory')
def inventory_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    lang = session.get('language', 'en')
    inventory = load_inventory()
    items = inventory['items']
    total_items = len(items)
    low_stock = [item for item in items if item['quantity'] <= 2]
    return render_template('inventory.html',
                           username=session['username'],
                           items=items,
                           total_items=total_items,
                           low_stock=low_stock,
                           lang=lang,
                           text=get_text)


# ===== EXPIRY PAGE =====
@app.route('/expiry')
def expiry_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    lang = session.get('language', 'en')
    inventory = load_inventory()
    items = inventory['items']
    today = datetime.now().date()
    expiring = []
    for item in items:
        try:
            expiry_date = datetime.strptime(item['expiry'], '%Y-%m-%d').date()
            days_left = (expiry_date - today).days
            if 0 <= days_left <= 7:
                expiring.append({**item, 'days_left': days_left})
        except:
            pass
    expiring.sort(key=lambda x: x['days_left'])
    return render_template('expiry.html',
                           username=session['username'],
                           expiring=expiring,
                           lang=lang,
                           text=get_text)


# ===== SHOPPING LIST PAGE =====
@app.route('/shopping')
def shopping_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    lang = session.get('language', 'en')
    inventory = load_inventory()
    items = inventory['items']
    low_stock = [item for item in items if item['quantity'] <= 2]
    return render_template('shopping.html',
                           username=session['username'],
                           low_stock=low_stock,
                           lang=lang,
                           text=get_text)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ===== API ROUTES =====
@app.route('/api/inventory', methods=['GET', 'POST'])
def api_inventory():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    if request.method == 'GET':
        return jsonify(load_inventory())
    elif request.method == 'POST':
        data = request.json
        inventory = load_inventory()
        new_item = {
            'id': inventory['next_id'],
            'name': data['name'],
            'quantity': int(data['quantity']),
            'unit': data['unit'],
            'expiry': data['expiry'],
            'category': data['category']
        }
        inventory['items'].append(new_item)
        inventory['next_id'] += 1
        save_inventory(inventory)
        return jsonify({'success': True, 'item': new_item})

@app.route('/api/inventory/<int:item_id>', methods=['PUT'])
def api_inventory_item(item_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    inventory = load_inventory()
    item = next((i for i in inventory['items'] if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    data = request.json
    if 'quantity' in data:
        item['quantity'] = int(data['quantity'])
    save_inventory(inventory)
    return jsonify({'success': True, 'item': item})

@app.route('/api/predict')
def api_predict():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    predictions = {
        'usage': [
            {'item': 'Milk', 'prediction': '+12%', 'confidence': 0.85},
            {'item': 'Eggs', 'prediction': '-4%', 'confidence': 0.78},
            {'item': 'Bread', 'prediction': '+8%', 'confidence': 0.82}
        ],
        'expense_forecast': 145,
        'waste_reduction': '23%',
        'recommendations': [
            'Buy milk in bulk to save 15%',
            'Use eggs within 5 days to avoid waste',
            'Consider freezing bread for longer storage'
        ]
    }
    return jsonify(predictions)

@app.route('/api/pantry-nutrition')
def pantry_nutrition():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    inventory = load_inventory()
    items = inventory['items']
    total_nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}
    nutrition_data = {
        'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'fiber': 4.4},
        'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'fiber': 3.1},
        'egg': {'calories': 78, 'protein': 6, 'carbs': 0.6, 'fat': 5, 'fiber': 0},
        'milk': {'calories': 149, 'protein': 8, 'carbs': 12, 'fat': 8, 'fiber': 0},
        'bread': {'calories': 265, 'protein': 9, 'carbs': 50, 'fat': 3.2, 'fiber': 2.4},
        'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0},
        'rice': {'calories': 206, 'protein': 4.3, 'carbs': 45, 'fat': 0.4, 'fiber': 0.6},
        'cheese': {'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'fiber': 0},
        'tomato': {'calories': 22, 'protein': 1.1, 'carbs': 4.8, 'fat': 0.2, 'fiber': 1.5},
        'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7},
        'carrot': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8},
        'potato': {'calories': 77, 'protein': 2, 'carbs': 17, 'fat': 0.1, 'fiber': 2.2},
    }
    for item in items:
        item_lower = item['name'].lower()
        for key in nutrition_data:
            if key in item_lower:
                qty = item['quantity']
                for k in ['calories', 'protein', 'carbs', 'fat', 'fiber']:
                    total_nutrition[k] += nutrition_data[key][k] * qty
                break
    return jsonify({'success': True, 'total_nutrition': total_nutrition})

# ============================================
# RECIPE PLANNER — FULL FEATURE SYSTEM
# ============================================

RECIPES = [
    {
        "id": 1, "name": "Veggie Omelette", "emoji": "🍳",
        "category": "Breakfast", "difficulty": "Easy", "cook_time": 10, "servings": 2,
        "ingredients": [
            {"name": "Eggs", "quantity": 3, "unit": "pcs"},
            {"name": "Tomatoes", "quantity": 1, "unit": "pcs"},
            {"name": "Onions", "quantity": 1, "unit": "pcs"},
            {"name": "Salt", "quantity": 1, "unit": "pinch"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"}
        ],
        "steps": [
            "Crack eggs into a bowl and whisk with salt.",
            "Chop tomatoes and onions finely.",
            "Heat oil in a pan over medium heat.",
            "Sauté onions until golden, add tomatoes.",
            "Pour eggs into the pan and cook until set.",
            "Fold the omelette and serve hot."
        ],
        "nutrition": {"calories": 210, "protein": 14, "carbs": 6, "fat": 15, "fiber": 1.5},
        "tips": "Add cheese for extra flavor. Use low heat for fluffy omelette."
    },
    {
        "id": 2, "name": "Tomato Salad", "emoji": "🥗",
        "category": "Lunch", "difficulty": "Easy", "cook_time": 5, "servings": 2,
        "ingredients": [
            {"name": "Tomatoes", "quantity": 3, "unit": "pcs"},
            {"name": "Onions", "quantity": 1, "unit": "pcs"},
            {"name": "Olive Oil", "quantity": 2, "unit": "tbsp"},
            {"name": "Salt", "quantity": 1, "unit": "pinch"},
            {"name": "Pepper", "quantity": 1, "unit": "pinch"}
        ],
        "steps": [
            "Wash and chop tomatoes into cubes.",
            "Slice onions thinly.",
            "Mix tomatoes and onions in a bowl.",
            "Add olive oil, salt and pepper.",
            "Toss gently and serve fresh."
        ],
        "nutrition": {"calories": 120, "protein": 2, "carbs": 8, "fat": 9, "fiber": 2.2},
        "tips": "Chill for 10 minutes for best taste. Add basil for aroma."
    },
    {
        "id": 3, "name": "Grilled Cheese Sandwich", "emoji": "🧀",
        "category": "Snack", "difficulty": "Easy", "cook_time": 8, "servings": 1,
        "ingredients": [
            {"name": "Bread", "quantity": 2, "unit": "slices"},
            {"name": "Cheese", "quantity": 2, "unit": "slices"},
            {"name": "Butter", "quantity": 1, "unit": "tbsp"}
        ],
        "steps": [
            "Butter one side of each bread slice.",
            "Place cheese between the slices (buttered side out).",
            "Heat a pan over medium heat.",
            "Grill the sandwich until golden brown on both sides.",
            "Cut diagonally and serve hot."
        ],
        "nutrition": {"calories": 380, "protein": 12, "carbs": 34, "fat": 22, "fiber": 1.8},
        "tips": "Use low heat so cheese melts without burning bread."
    },
    {
        "id": 4, "name": "Apple Crumble", "emoji": "🍎",
        "category": "Dessert", "difficulty": "Medium", "cook_time": 35, "servings": 4,
        "ingredients": [
            {"name": "Apples", "quantity": 4, "unit": "pcs"},
            {"name": "Flour", "quantity": 1, "unit": "cup"},
            {"name": "Sugar", "quantity": 1, "unit": "cup"},
            {"name": "Butter", "quantity": 100, "unit": "g"},
            {"name": "Cinnamon", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            "Preheat oven to 180°C.",
            "Peel and slice apples.",
            "Mix apples with half sugar and cinnamon.",
            "In another bowl, mix flour, remaining sugar and butter.",
            "Place apples in a baking dish, top with crumble mixture.",
            "Bake for 30 minutes until golden.",
            "Serve warm with ice cream."
        ],
        "nutrition": {"calories": 420, "protein": 4, "carbs": 62, "fat": 18, "fiber": 3.2},
        "tips": "Add oats to the crumble for extra crunch."
    },
    {
        "id": 5, "name": "Pasta Arrabbiata", "emoji": "🍝",
        "category": "Dinner", "difficulty": "Medium", "cook_time": 25, "servings": 3,
        "ingredients": [
            {"name": "Pasta", "quantity": 250, "unit": "g"},
            {"name": "Tomatoes", "quantity": 4, "unit": "pcs"},
            {"name": "Garlic", "quantity": 3, "unit": "cloves"},
            {"name": "Olive Oil", "quantity": 2, "unit": "tbsp"},
            {"name": "Chili Flakes", "quantity": 1, "unit": "tsp"},
            {"name": "Salt", "quantity": 1, "unit": "pinch"}
        ],
        "steps": [
            "Boil pasta in salted water until al dente.",
            "Heat oil, sauté chopped garlic and chili flakes.",
            "Add crushed tomatoes and cook for 10 minutes.",
            "Add salt and mix the sauce.",
            "Toss pasta into the sauce.",
            "Serve hot with grated cheese."
        ],
        "nutrition": {"calories": 380, "protein": 12, "carbs": 68, "fat": 8, "fiber": 4.1},
        "tips": "Save pasta water to adjust sauce consistency."
    },
    {
        "id": 6, "name": "Chicken Curry", "emoji": "🍛",
        "category": "Dinner", "difficulty": "Hard", "cook_time": 45, "servings": 4,
        "ingredients": [
            {"name": "Chicken", "quantity": 500, "unit": "g"},
            {"name": "Onions", "quantity": 2, "unit": "pcs"},
            {"name": "Tomatoes", "quantity": 2, "unit": "pcs"},
            {"name": "Ginger Garlic Paste", "quantity": 2, "unit": "tbsp"},
            {"name": "Curry Powder", "quantity": 2, "unit": "tsp"},
            {"name": "Oil", "quantity": 3, "unit": "tbsp"}
        ],
        "steps": [
            "Heat oil, sauté chopped onions until golden.",
            "Add ginger garlic paste and cook for 1 minute.",
            "Add tomatoes and cook until soft.",
            "Add curry powder and mix well.",
            "Add chicken pieces and coat with masala.",
            "Add water, cover and cook for 25 minutes.",
            "Garnish with coriander and serve with rice."
        ],
        "nutrition": {"calories": 480, "protein": 38, "carbs": 12, "fat": 30, "fiber": 2.5},
        "tips": "Marinate chicken for 30 minutes for deeper flavor."
    }
]

def _recipe_match(recipe, inventory_names):
    available_count = 0
    for ing in recipe['ingredients']:
        ing_lower = ing['name'].lower()
        if any(ing_lower in inv or inv in ing_lower for inv in inventory_names):
            available_count += 1
    total = len(recipe['ingredients'])
    return {
        **recipe,
        'available_count': available_count,
        'total_count': total,
        'match_percent': round((available_count / total) * 100) if total else 0,
        'ready_to_cook': available_count == total
    }

@app.route('/recipes')
def recipes():
    if 'username' not in session:
        return redirect(url_for('login'))
    lang = session.get('language', 'en')
    return render_template('recipes.html',
                           username=session['username'],
                           recipes=RECIPES,
                           lang=lang,
                           text=get_text)

@app.route('/api/recipes')
def api_recipes():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'success': True, 'recipes': RECIPES})

@app.route('/api/recipes/<int:recipe_id>')
def api_recipe_detail(recipe_id):
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    recipe = next((r for r in RECIPES if r['id'] == recipe_id), None)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    inventory = load_inventory()
    inventory_names = [item['name'].lower() for item in inventory['items']]
    ingredients_status = []
    available_count = 0
    for ing in recipe['ingredients']:
        ing_lower = ing['name'].lower()
        is_available = any(ing_lower in inv or inv in ing_lower for inv in inventory_names)
        if is_available:
            available_count += 1
        ingredients_status.append({
            'name': ing['name'],
            'quantity': ing['quantity'],
            'unit': ing['unit'],
            'available': is_available
        })
    match_percent = round((available_count / len(recipe['ingredients'])) * 100) if recipe['ingredients'] else 0
    return jsonify({
        'success': True,
        'recipe': {
            **recipe,
            'ingredients_status': ingredients_status,
            'available_count': available_count,
            'total_count': len(recipe['ingredients']),
            'match_percent': match_percent,
            'ready_to_cook': available_count == len(recipe['ingredients'])
        }
    })

@app.route('/api/recipes/filter')
def api_recipes_filter():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    category = request.args.get('category', 'all')
    difficulty = request.args.get('difficulty', 'all')
    max_time = request.args.get('max_time', 'all')
    search = request.args.get('search', '').lower()
    inventory = load_inventory()
    inventory_names = [item['name'].lower() for item in inventory['items']]
    filtered = RECIPES
    if category != 'all':
        filtered = [r for r in filtered if r['category'] == category]
    if difficulty != 'all':
        filtered = [r for r in filtered if r['difficulty'] == difficulty]
    if max_time != 'all':
        try:
            filtered = [r for r in filtered if r['cook_time'] <= int(max_time)]
        except:
            pass
    if search:
        filtered = [r for r in filtered
                    if search in r['name'].lower()
                    or any(search in ing['name'].lower() for ing in r['ingredients'])]
    result = [_recipe_match(r, inventory_names) for r in filtered]
    return jsonify({'success': True, 'recipes': result, 'count': len(result)})

@app.route('/api/recipes/random')
def api_random_recipe():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        recipe = random.choice(RECIPES)
        return jsonify({'success': True, 'recipe': recipe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/recipes/suggest-by-expiry')
def api_recipes_by_expiry():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    inventory = load_inventory()
    items = inventory['items']
    inventory_names = [i['name'].lower() for i in items]
    today = datetime.now().date()
    expiring_names = []
    for it in items:
        try:
            exp = datetime.strptime(it['expiry'], '%Y-%m-%d').date()
            days = (exp - today).days
            if 0 <= days <= 5:
                expiring_names.append(it['name'].lower())
        except:
            pass
    scored = []
    for r in RECIPES:
        matched = _recipe_match(r, inventory_names)
        expiry_bonus = 0
        for ing in r['ingredients']:
            ing_low = ing['name'].lower()
            if any(ing_low in exp or exp in ing_low for exp in expiring_names):
                expiry_bonus += 1
        scored.append({**matched, 'expiry_bonus': expiry_bonus})
    scored.sort(key=lambda x: (x['expiry_bonus'], x['available_count']), reverse=True)
    return jsonify({'success': True, 'recipes': scored})

@app.route('/api/favorites', methods=['GET', 'POST'])
def api_favorites():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    users = load_users()
    username = session['username']
    if request.method == 'GET':
        favs = users.get(username, {}).get('favorites', [])
        return jsonify({'success': True, 'favorites': favs})
    data = request.json or {}
    rid = data.get('recipe_id')
    if rid is None:
        return jsonify({'error': 'Missing recipe_id'}), 400
    users.setdefault(username, {})
    users[username].setdefault('favorites', [])
    favs = users[username]['favorites']
    if rid in favs:
        favs.remove(rid)
        toggled = False
    else:
        favs.append(rid)
        toggled = True
    save_users(users)
    return jsonify({'success': True, 'favorites': favs, 'added': toggled})

@app.route('/api/history', methods=['GET', 'POST'])
def api_history():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    users = load_users()
    username = session['username']
    if request.method == 'GET':
        hist = users.get(username, {}).get('recipe_history', [])
        enriched = []
        for rid in hist:
            r = next((x for x in RECIPES if x['id'] == rid), None)
            if r:
                enriched.append({'id': r['id'], 'name': r['name'], 'emoji': r['emoji']})
        return jsonify({'success': True, 'history': enriched})
    data = request.json or {}
    rid = data.get('recipe_id')
    if rid is None:
        return jsonify({'error': 'Missing recipe_id'}), 400
    users.setdefault(username, {})
    users[username].setdefault('recipe_history', [])
    hist = users[username]['recipe_history']
    if rid in hist:
        hist.remove(rid)
    hist.insert(0, rid)
    users[username]['recipe_history'] = hist[:10]
    save_users(users)
    return jsonify({'success': True, 'history': users[username]['recipe_history']})

# ===== SUBSCRIBE =====
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    print(f"New subscriber: {email}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)