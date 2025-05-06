from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db = SQLAlchemy(app)

# ---------------------
# Database Models
# ---------------------

# Employees (common)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # admin or staff

# RESTAURANT
class RestaurantMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class RestaurantOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# GROCERY
class GroceryMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class GroceryOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


@app.route('/admin')
def admin():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    restaurant_orders = RestaurantOrder.query.all()
    grocery_orders = GroceryOrder.query.all()
    clothing_orders = ClothingOrder.query.all()
    stationary_orders = StationaryOrder.query.all()
    fruits_orders = FruitsVegOrder.query.all()

    total_sales = {
        "Restaurant": sum(order.price for order in restaurant_orders),
        "Grocery Store": sum(order.price for order in grocery_orders),
        "Clothing Store": sum(order.price for order in clothing_orders),
        "Stationary Shop": sum(order.price for order in stationary_orders),
        "Fruits & Vegetables": sum(order.price for order in fruits_orders)
    }

    return render_template(
        'admin.html',
        restaurant_orders=restaurant_orders,
        grocery_orders=grocery_orders,
        clothing_orders=clothing_orders,
        stationary_orders=stationary_orders,
        fruits_orders=fruits_orders,
        total_sales=total_sales
    )

# ---------------------
# Master Routes
# ---------------------

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/navigate', methods=['POST'])
def navigate():
    business_type = request.form['business_type']
    return redirect(url_for(f'{business_type}_index'))

# ---------------------
# Restaurant Routes
# ---------------------

@app.route('/restaurant')
def restaurant_index():
    menu = RestaurantMenuItem.query.all()
    return render_template(
        'index.html',
        menu=menu,
        business_name="Restaurant",
        order_route="restaurant_order",
        add_item_route="restaurant_add_item"
    )

@app.route('/restaurant/order/<int:item_id>')
def restaurant_order(item_id):
    item = RestaurantMenuItem.query.get(item_id)
    new_order = RestaurantOrder(item_name=item.name, price=item.price)
    db.session.add(new_order)
    db.session.commit()
    flash(f"Ordered {item.name} from restaurant!", "success")
    return redirect(url_for('restaurant_index'))

@app.route('/restaurant/add_item', methods=['GET', 'POST'])
def restaurant_add_item():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        item = RestaurantMenuItem(name=name, price=price)
        db.session.add(item)
        db.session.commit()
        flash(f"{name} added to restaurant!", "success")
        return redirect(url_for('restaurant_index'))
    return render_template('add_item.html')

# ---------------------
# Grocery Routes
# ---------------------


@app.route('/grocery')
def grocery_index():
    menu = GroceryMenuItem.query.all()
    return render_template(
        'index.html',
        menu=menu,
        business_name="Grocery Store",
        order_route="grocery_order",
        add_item_route="grocery_add_item"
    )

@app.route('/grocery/order/<int:item_id>')
def grocery_order(item_id):
    item = GroceryMenuItem.query.get(item_id)
    new_order = GroceryOrder(item_name=item.name, price=item.price)
    db.session.add(new_order)
    db.session.commit()
    flash(f"Ordered {item.name} from grocery!", "success")
    return redirect(url_for('grocery_index'))

@app.route('/grocery/add_item', methods=['GET', 'POST'])
def grocery_add_item():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        item = GroceryMenuItem(name=name, price=price)
        db.session.add(item)
        db.session.commit()
        flash(f"{name} added to grocery store!", "success")
        return redirect(url_for('grocery_index'))
    return render_template('add_item.html')



# ---------------------
# Clothing Store Routes
# ---------------------

class ClothingMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class ClothingOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/clothing')
def clothing_index():
    menu = ClothingMenuItem.query.all()
    return render_template(
        'index.html',
        menu=menu,
        business_name="Clothing Store",
        order_route="clothing_order",
        add_item_route="clothing_add_item"
    )

@app.route('/clothing/order/<int:item_id>')
def clothing_order(item_id):
    item = ClothingMenuItem.query.get(item_id)
    new_order = ClothingOrder(item_name=item.name, price=item.price)
    db.session.add(new_order)
    db.session.commit()
    flash(f"Ordered {item.name} from clothing store!", "success")
    return redirect(url_for('clothing_index'))

@app.route('/clothing/add_item', methods=['GET', 'POST'])
def clothing_add_item():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        item = ClothingMenuItem(name=name, price=price)
        db.session.add(item)
        db.session.commit()
        flash(f"{name} added to clothing store!", "success")
        return redirect(url_for('clothing_index'))
    return render_template('add_item.html')


# ---------------------
# Stationary Shop Routes
# ---------------------

class StationaryMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class StationaryOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/stationary')
def stationary_index():
    menu = StationaryMenuItem.query.all()
    return render_template(
        'index.html',
        menu=menu,
        business_name="Stationary Shop",
        order_route="stationary_order",
        add_item_route="stationary_add_item"
    )

@app.route('/stationary/order/<int:item_id>')
def stationary_order(item_id):
    item = StationaryMenuItem.query.get(item_id)
    new_order = StationaryOrder(item_name=item.name, price=item.price)
    db.session.add(new_order)
    db.session.commit()
    flash(f"Ordered {item.name} from stationary shop!", "success")
    return redirect(url_for('stationary_index'))

@app.route('/stationary/add_item', methods=['GET', 'POST'])
def stationary_add_item():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        item = StationaryMenuItem(name=name, price=price)
        db.session.add(item)
        db.session.commit()
        flash(f"{name} added to stationary shop!", "success")
        return redirect(url_for('stationary_index'))
    return render_template('add_item.html')


# ---------------------
# Fruits & Vegetables Routes
# ---------------------

class FruitsVegMenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class FruitsVegOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/fruits_vegetables')
def fruits_vegetables_index():
    menu = FruitsVegMenuItem.query.all()
    return render_template(
        'index.html',
        menu=menu,
        business_name="Fruits & Vegetables",
        order_route="fruits_vegetables_order",
        add_item_route="fruits_vegetables_add_item"
    )

@app.route('/fruits_vegetables/order/<int:item_id>')
def fruits_vegetables_order(item_id):
    item = FruitsVegMenuItem.query.get(item_id)
    new_order = FruitsVegOrder(item_name=item.name, price=item.price)
    db.session.add(new_order)
    db.session.commit()
    flash(f"Ordered {item.name} from fruits & vegetables!", "success")
    return redirect(url_for('fruits_vegetables_index'))

@app.route('/fruits_vegetables/add_item', methods=['GET', 'POST'])
def fruits_vegetables_add_item():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        item = FruitsVegMenuItem(name=name, price=price)
        db.session.add(item)
        db.session.commit()
        flash(f"{name} added to fruits & vegetables!", "success")
        return redirect(url_for('fruits_vegetables_index'))
    return render_template('add_item.html')


# ---------------------
# Auth & Admin
# ---------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Employee.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user'] = username
            session['role'] = user.role
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

# ---------------------
# Database Initialization
# ---------------------

with app.app_context():
    db.create_all()

    if not Employee.query.filter_by(username="admin").first():
        password = generate_password_hash("admin123", method='pbkdf2:sha256')
        admin = Employee(username="admin", password_hash=password, role="admin")
        db.session.add(admin)

    if not RestaurantMenuItem.query.first():
        db.session.add_all([
            RestaurantMenuItem(name="Pizza", price=12.99),
            RestaurantMenuItem(name="Burger", price=8.99)
        ])

    if not GroceryMenuItem.query.first():
        db.session.add_all([
            GroceryMenuItem(name="Milk", price=2.99),
            GroceryMenuItem(name="Bread", price=1.49)
        ])


    if not ClothingMenuItem.query.first():
        db.session.add_all([
        ClothingMenuItem(name="T-Shirt", price=15.99),
        ClothingMenuItem(name="Jeans", price=39.99)
    ])

    if not StationaryMenuItem.query.first():
       db.session.add_all([
        StationaryMenuItem(name="Notebook", price=2.49),
        StationaryMenuItem(name="Pens Pack", price=1.99)
    ])

    if not FruitsVegMenuItem.query.first():
       db.session.add_all([
        FruitsVegMenuItem(name="Bananas (1kg)", price=1.49),
        FruitsVegMenuItem(name="Tomatoes (1kg)", price=1.89)
    ])

    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
