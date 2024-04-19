import os
import csv
from datetime import datetime, time, timedelta
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)  # Or another secret key
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///food_delivery.db")

def create_tables():

    # Create restaurant table
    db.execute("""
        CREATE TABLE IF NOT EXISTS restaurant (
            r_id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            cuisineType VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        );
    """)

    # Create customer table
    db.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            id INTEGER PRIMARY KEY,
            customer_name VARCHAR(255),
            address VARCHAR(255),
            contact_phone VARCHAR(255),
            email VARCHAR(255),
            confirmation_code VARCHAR(255),
            password VARCHAR,
            time_joined TIMESTAMP,
            cash DECIMAL(12,2)
        );
    """)

    # Create placed_order table
    db.execute("""
        CREATE TABLE IF NOT EXISTS placed_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_time TIMESTAMP,
            estimated_delivery_time TIMESTAMP,
            food_ready TIMESTAMP,
            actual_delivery_time TIMESTAMP,
            delivery_address VARCHAR(255),
            customer_id INTEGER,
            price DECIMAL(12, 2),
            discount DECIMAL(12, 2),
            final_price DECIMAL(12, 2),
            comment TEXT,
            ts TIMESTAMP,
            Restaurant_r_id INTEGER,
            FOREIGN KEY (customer_id) REFERENCES customer(id),
            FOREIGN KEY (Restaurant_r_id) REFERENCES restaurant(r_id)
        );
    """)
    #Create comment table
    db.execute("""
        CREATE TABLE IF NOT EXISTS comment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placed_order_id INTEGER NOT NULL,
            comment_text TEXT,
            ts TIMESTAMP,
            is_complaint BOOLEAN,
            is_praise BOOLEAN,
            rating DECIMAL(12, 2),
            FOREIGN KEY (placed_order_id) REFERENCES placed_order(id)
        );
    """)
    # Create offer table
    db.execute("""
        CREATE TABLE IF NOT EXISTS offer (
            id INTEGER PRIMARY KEY,
            date_active_from DATE NOT NULL,
            time_active_from TIME NOT NULL,
            date_active_to DATE NOT NULL,
            time_active_to TIME NOT NULL,
            offer_price DECIMAL(12, 2)
        );
    """)

    # Create menu_item table
    db.execute("""
        CREATE TABLE IF NOT EXISTS menu_item (
            id INTEGER PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            price DECIMAL(12, 2) NOT NULL,
            active BOOLEAN,
            Restaurant_r_id INTEGER,
            FOREIGN KEY (Restaurant_r_id) REFERENCES restaurant(r_id)
        );
    """)

    # Create order_status table
    db.execute("""
        CREATE TABLE IF NOT EXISTS order_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placed_order_id INTEGER NOT NULL,
            status VARCHAR(255) NOT NULL,
            ts TIMESTAMP NOT NULL,
            FOREIGN KEY (placed_order_id) REFERENCES placed_order(id)
        );
    """)
    # Create in_offer table
    db.execute("""
        CREATE TABLE IF NOT EXISTS in_offer (
            id INTEGER PRIMARY KEY,
            offer_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            FOREIGN KEY (offer_id) REFERENCES offer(id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
        );
    """)

    # Create in_order table
    db.execute("""
        CREATE TABLE IF NOT EXISTS in_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placed_order_id INTEGER NOT NULL,
            offer_id INTEGER,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            item_price DECIMAL(12, 2),
            FOREIGN KEY (placed_order_id) REFERENCES placed_order(id),
            FOREIGN KEY (offer_id) REFERENCES offer(id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
        );
    """)


@app.before_first_request
            
def initialize():
    # Create tables and load data if needed
    #create_tables()
    load_data_if_needed()

def load_data_if_needed():
    # Check if the data is already loaded
    restaurant_count = db.execute("SELECT COUNT(*) FROM restaurant")
    menu_item_count = db.execute("SELECT COUNT(*) FROM menu_item")
    offer_count = db.execute("SELECT COUNT(*) FROM offer")
    in_offer_count = db.execute("SELECT COUNT(*) FROM in_offer")
    if restaurant_count[0]['COUNT(*)'] == 0:
        preload_restaurants()
    if menu_item_count[0]['COUNT(*)'] == 0:
        preload_menu_items()
    if offer_count[0]['COUNT(*)'] == 0:
        preload_offers()
    if in_offer_count[0]['COUNT(*)'] == 0:
        preload_in_offer()

def preload_restaurants():
    with open('data/restaurants.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.execute("INSERT INTO restaurant (name, location, cuisineType, password, email) VALUES (:name, :location, :cuisineType, :password, :email)",
                       name=row['name'], location=row['location'], cuisineType=row['cuisineType'], password=row['password'], email=row['email'])

def preload_offers():
    with open('data/offer.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.execute("INSERT INTO offer (id, date_active_from, time_active_from, date_active_to, time_active_to, offer_price) VALUES (:id, :date_active_from, :time_active_from, :date_active_to, :time_active_to, :offer_price)",
                       id = row['id'], date_active_from=row['date_active_from'], time_active_from=row['time_active_from'], date_active_to=row['date_active_to'], time_active_to=row['time_active_to'], offer_price=row['offer_price'])

def preload_menu_items():
    with open('data/menu_item.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.execute("INSERT INTO menu_item (id, item_name, price, active, Restaurant_r_id) VALUES (:id, :item_name, :price, :active,:Restaurant_r_id)",
                       id = row['id'], item_name=row['item_name'], price=row['price'], active=row['active'], Restaurant_r_id=row['Restaurant_r_id'])
 
def preload_in_offer():
    with open('data/in_offer.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.execute("INSERT INTO in_offer (id, offer_id, menu_item_id) VALUES(:id, :offer_id, :menu_item_id)",
                       id = row['id'], offer_id = row['offer_id'], menu_item_id=row['menu_item_id'])
        
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def default_page():

    return render_template("dashboard.html")

@app.route("/homepage")
@login_required
def home():
    try:
        customer_details = db.execute("""
            SELECT id, customer_name, address, contact_phone, email, time_joined, cash
            FROM customer
            WHERE id = ? 
        """, (user_c_id))

        # Pass the data to the menu template
        return render_template("home.html", customer_details= customer_details)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        # Return an error message to the user
        return render_template("error.html", message="An internal server error occurred.")
    

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    user_id = user_c_id  # Ensure user_c_id is defined and accessible, typically from the session
    customer_info = db.execute("SELECT cash FROM customer WHERE id = ?", user_id)
    if not customer_info:
        return apology("Customer not found", 403)  # Or handle the error appropriately

    if request.method == "POST":
        try:
            additional_cash = float(request.form.get("cash"))
        except ValueError:
            return apology("Please enter a numerical value!")
        
        current_cash = customer_info[0]["cash"]
        updated_cash = current_cash + additional_cash
        db.execute("UPDATE customer SET cash = ? WHERE id = ?", updated_cash, user_id)
        flash("Cash added successfully.")
        return redirect(url_for('addcash'))
    else:
        return render_template("addcash.html", current_cash=customer_info[0]["cash"])

    
@app.route("/restaurants", methods=["GET", "POST"])
def restaurants_view():
    # Set a default pattern that matches everything
    pattern = "%%"  # This is SQL for 'match any character sequence'
    if request.method == "POST":
        # Retrieve the cuisine type from the form data
        cuisine_type = request.form.get("cuisineType")
        if cuisine_type:  # Check if the cuisine type field is not empty
            pattern = f"%{cuisine_type}%"
    
    # Fetch restaurants that match the cuisine type pattern
    restaurants = db.execute("SELECT * FROM restaurant WHERE cuisineType LIKE ?", (pattern,))
    
    # Pass the data to the template
    return render_template("restaurants.html", restaurants=restaurants)

@app.route("/search_food_item", methods=["GET", "POST"])
@login_required
def search_food_item():
    if request.method == "POST":
        search_query = request.form.get("food_item")
        results = db.execute("""
            SELECT r.name, r.location, r.cuisineType, mi.item_name, mi.price, r.r_id AS restaurant_id
            FROM menu_item mi
            JOIN restaurant r ON mi.Restaurant_r_id = r.r_id
            WHERE mi.item_name LIKE ? AND mi.active = 'TRUE'
        """, ("%"+search_query+"%",))
        return render_template("search_results.html", results=results)
    else:
        return render_template("search_food_item.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("id"):
            return apology("must provide id", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM customer WHERE id = ?", request.form.get("id"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        global user_c_id;
        user_c_id = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/withdrawcash", methods=["GET", "POST"])
@login_required
def withdrawcash():
    customer_id = user_c_id  # make sure this variable is available in the session or globally
    customer = db.execute("SELECT cash FROM customer WHERE id = ?", customer_id)[0]

    if request.method == "POST":
        try:
            withdrawal_amount = float(request.form.get("cash"))
        except ValueError:
            return apology("Please enter a numerical value!")

        if withdrawal_amount > customer["cash"]:
            return apology("Not enough cash in your account.")
        else:
            updated_cash = customer["cash"] - withdrawal_amount
            db.execute("UPDATE customer SET cash = ? WHERE id = ?", updated_cash, customer_id)
            flash('Cash withdrawal successful.')
            return redirect(url_for('withdrawcash'))  # to prevent form resubmission
    else:
        return render_template("withdrawcash.html", current_cash=customer["cash"])
@app.route("/select_restaurant_for_stats", methods=["GET"])
@login_required
def select_restaurant_for_stats():
    restaurants = db.execute("SELECT r_id, name FROM restaurant")
    return render_template("select_restaurant_for_stats.html", restaurants=restaurants)

@app.route("/restaurant_stats", methods=["POST"])
@login_required
def restaurant_stats():
    restaurant_id = request.form.get("restaurant_id")
    stats = fetch_stats(restaurant_id)
    return render_template("restaurant_stats.html", stats=stats)

def fetch_stats(restaurant_id):
    stats = db.execute("""
        SELECT r.name, 
               AVG(c.rating) as avg_rating, 
               SUM(io.quantity * io.item_price) as total_sales, 
               COUNT(distinct po.id) as total_orders
        FROM restaurant r
        LEFT JOIN placed_order po ON r.r_id = po.Restaurant_r_id
        LEFT JOIN in_order io ON po.id = io.placed_order_id
        LEFT JOIN comment c ON po.id = c.placed_order_id
        WHERE r.r_id = ?
        GROUP BY r.r_id
    """, restaurant_id)
    return stats[0]

@app.route("/user_stats")
@login_required
def user_stats():
    user_id = session["user_id"]

    # Adjusted SQL query to calculate statistics without direct customer_id in comment table
    user_stats = db.execute("""
    SELECT 
        r.name AS restaurant_name, 
        COUNT(po.id) AS number_of_orders, 
        SUM(po.final_price) AS total_spent, 
        AVG(c.rating) AS avg_rating
    FROM placed_order po
    INNER JOIN restaurant r ON po.Restaurant_r_id = r.r_id
    LEFT JOIN comment c ON po.id = c.placed_order_id
    WHERE po.customer_id = ?
    GROUP BY r.name
    """, user_id)

    return render_template("user_stats.html", user_stats=user_stats)

@app.route("/order", methods=["GET", "POST"])
@login_required
def order():
    if request.method == "POST":
        cuisine_type = request.form.get("cuisineType")
        # Use %% to escape % in the string format for SQL query
        pattern = f"%{cuisine_type}%"
        restaurants = db.execute("SELECT * FROM restaurant WHERE cuisineType LIKE ?", (pattern,))
        return render_template("select_restaurant.html", restaurants=restaurants)
    else:
        # If it's a GET request, display all restaurants or handle accordingly
        restaurants = db.execute("SELECT * FROM restaurant")
        return render_template("select_restaurant.html", restaurants=restaurants)

@app.route("/menu/<int:restaurant_id>")
@login_required
def menu(restaurant_id):
    restaurant = db.execute("SELECT name FROM restaurant WHERE r_id = ?", restaurant_id)
    restaurant_name = restaurant[0]['name'] if restaurant else 'Restaurant'
    # Fetch the menu items that are active for the selected restaurant
    try:
        menu_items = db.execute("""
            SELECT id, item_name, price
            FROM menu_item
            WHERE Restaurant_r_id = ? AND (active = 'TRUE' OR active = 1)
        """, (restaurant_id,))

        # Pass the data to the menu template
        return render_template("menu.html", menu_items=menu_items, restaurant_id=restaurant_id, restaurant_name=restaurant_name)
    
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")
        # Return an error message to the user
        return render_template("error.html", message="An internal server error occurred.")
    
@app.route("/offers")
@login_required
def offers():
    current_datetime = datetime.now()
    # Get a unique list of restaurants with active offers
    restaurants_with_offers = db.execute("""
        SELECT DISTINCT r.r_id, r.name, r.location, r.cuisineType, r.email
        FROM restaurant r
        INNER JOIN menu_item mi ON r.r_id = mi.Restaurant_r_id
        INNER JOIN in_offer io ON mi.id = io.menu_item_id
        INNER JOIN offer o ON io.offer_id = o.id
        WHERE (mi.active = 'TRUE' OR mi.active = 1)
        AND o.date_active_from <= ? 
        AND o.date_active_to >= ? 
    """, current_datetime.date(), current_datetime.date())

    return render_template("restaurants_with_offers.html", restaurants=restaurants_with_offers)

@app.route("/offers/<int:restaurant_id>")
@login_required
def restaurant_offers(restaurant_id):
    current_datetime = datetime.now()
    # Get all active offers for the selected restaurant
    active_offers = db.execute("""
        SELECT mi.id AS menu_item_id, mi.item_name, mi.price,
               o.offer_price, io.offer_id
        FROM menu_item mi
        JOIN in_offer io ON mi.id = io.menu_item_id
        JOIN offer o ON io.offer_id = o.id
        WHERE mi.Restaurant_r_id = ? 
        AND (mi.active = 'TRUE' OR mi.active = 1)
        AND o.date_active_from <= ? 
        AND o.date_active_to >= ? 
    """, restaurant_id, current_datetime.date(), current_datetime.date())

    return render_template("restaurant_offers.html", offers=active_offers, restaurant_id=restaurant_id)

@app.route("/confirm_order", methods=["POST"])
@login_required
def confirm_order():
    try:
        # Retrieve form data
        restaurant_id = request.form.get("restaurant_id")
        customer_id = user_c_id  # Assuming customer ID is stored in session
        
        # Fetch the customer's address from the database
        customer_info = db.execute("SELECT address,cash FROM customer WHERE id = ?", customer_id)
        if not customer_info:
            flash("Customer not found.", "error")
            return redirect(url_for('login'))  # Redirect to homepage if customer not found

        customer_address = customer_info[0]["address"]
        customer_cash = customer_info[0]["cash"]
        # Initialize the order total
        total_price = 0

        # Calculate total price based on items ordered
        for key, value in request.form.items():
            print(f"{key} , {value}")
            if key.startswith('quantity-') and int(value) > 0:
                item_id = key.split('-')[1]
                quantity = int(value)
                #print(f"Item id is {item_id}, quantity is {quantity}")
                # Get the price of the menu item
                menu_item_info = db.execute("SELECT price FROM menu_item WHERE id = ?", item_id)
                #print(menu_item_info)
                if menu_item_info:
                    menu_item_price = menu_item_info[0]['price']
                    total_price += menu_item_price * quantity
        #print(f"The total price is {total_price}")
        if(customer_cash < total_price):
            return render_template("not_enough_cash.html")
        else:
            new_cash_balance = customer_cash - total_price
            db.execute("UPDATE customer SET cash = ? WHERE id = ?", new_cash_balance, user_c_id)
        # Insert the order into the placed_order table
        order_time = datetime.now()
        db.execute("""
            INSERT INTO placed_order 
            (order_time, estimated_delivery_time, food_ready, actual_delivery_time, delivery_address, customer_id, price, discount, final_price, comment, ts, Restaurant_r_id) 
            VALUES (?, DATETIME(?, '+1 hour'), DATETIME(?, '+0.5 hour'), DATETIME(?, '+1 hour'), ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            order_time, order_time, order_time, order_time, customer_address, customer_id, total_price, 0, total_price, "Ok", order_time, restaurant_id)

        # Retrieve the ID of the order just inserted
        order_id_result = db.execute("SELECT last_insert_rowid()")
        order_id = order_id_result[0]["last_insert_rowid()"]
        
            # Define the status update times
        preparation_complete_time = order_time + timedelta(minutes=20)
        on_the_way_time = order_time + timedelta(minutes=25)
        delivery_time = order_time + timedelta(hours=1)

        # Insert the status updates for the order
        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'Order placed', order_time)
        
        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'Food preparation completed', preparation_complete_time)

        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'On the way', on_the_way_time)

        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'Delivered', delivery_time)
            # Insert each ordered item into in_order table
        for key, value in request.form.items():
            if key.startswith('quantity-') and int(value) > 0:
                item_id = key.split('-')[1]
                quantity = int(value)
                # Assuming menu_item_price is still available and valid
                menu_item_info = db.execute("SELECT price FROM menu_item WHERE id = ?", item_id)
                menu_item_price = menu_item_info[0]['price']
                db.execute("INSERT INTO in_order (placed_order_id, menu_item_id, quantity, item_price) VALUES (?, ?, ?, ?)",
                        order_id, item_id, quantity, menu_item_price)

    except Exception as e:
        print(e)  # Log the error for debugging
        flash("An error occurred while placing the order.", "error")
        return redirect(url_for('login'))  # Redirect to a safe page if error occurs

    # Redirect to an order confirmation page, passing order_id as a query parameter
    return redirect(url_for('order_confirmation', order_id=order_id))

@app.route("/confirm_order_offer", methods=["POST"])
@login_required
def confirm_order_offer():
    try:
        customer_id = user_c_id
        restaurant_id = request.form.get("restaurant_id")  # Get restaurant_id from the form
        order_items = []
        total_price = 0

        # Fetch the customer's address and current cash balance from the database
        customer_info = db.execute("SELECT address, cash FROM customer WHERE id = ?", customer_id)
        if not customer_info:
            flash("Customer not found.", "error")
            return redirect(url_for('home'))  # Assuming 'index' is your homepage view function

        customer_address = customer_info[0]['address']
        customer_cash = customer_info[0]['cash']
        quantity = 0
        # Extract item details and quantity from the form
        for key, value in request.form.items():
            print(f"{key},{value}")
            if key.startswith('quantity-'):
                item_id = key.split('-')[1]
                quantity = int(value)
                offer_id = request.form.get(f'offer_id-{item_id}', None)
                offer_price = request.form.get(f'offer_price-{item_id}', None)
            if key.startswith('offer_id-') and quantity > 0:
                offer_id = value
                item_id = key.split('-')[1]
                menu_item_info = db.execute("SELECT offer_price FROM offer, in_offer, menu_item WHERE offer.id = in_offer.id AND menu_item.id = in_offer.menu_item_id AND menu_item.id = ?", item_id)
                offer_price = menu_item_info[0]['offer_price']
                if offer_id and offer_price and quantity > 0:
                    offer_price = float(offer_price)
                    item_total_price = quantity * offer_price
                    total_price += item_total_price
                    order_items.append({'item_id': item_id, 'quantity': quantity, 'offer_id': offer_id, 'offer_price': offer_price})
        print(f"Total price {total_price}")
        # Check if the customer has enough cash to place the order
        if customer_cash < total_price:
            # Redirect to a page that informs the user about insufficient funds
            return render_template("not_enough_cash.html")

        # Insert the order into the placed_order table
        order_time = datetime.now()
        db.execute("""
            INSERT INTO placed_order 
            (order_time, estimated_delivery_time, food_ready, actual_delivery_time, delivery_address, customer_id, price, discount, final_price, comment, ts, Restaurant_r_id) 
            VALUES (?, DATETIME(?, '+1 hour'), DATETIME(?, '+0.5 hour'), DATETIME(?, '+1 hour'), ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            order_time, order_time, order_time, order_time, customer_address, customer_id, total_price, 0, total_price, "Ok", order_time, restaurant_id)
        
        # Update the customer's cash balance
        db.execute("UPDATE customer SET cash = ? WHERE id = ?", customer_cash-total_price, user_c_id)

        # Retrieve the ID of the order just inserted
        order_id_result = db.execute("SELECT last_insert_rowid()")
        order_id = order_id_result[0]["last_insert_rowid()"]
         # Define the status update times
        preparation_complete_time = order_time + timedelta(minutes=20)
        on_the_way_time = order_time + timedelta(minutes=25)
        delivery_time = order_time + timedelta(hours=1)

        # Insert the status updates for the order
        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'Order placed', order_time)
        
        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'Food preparation completed', preparation_complete_time)

        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'On the way', on_the_way_time)

        db.execute("""
            INSERT INTO order_status (placed_order_id, status, ts) VALUES (?, ?, ?)
            """, order_id, 'Delivered', delivery_time)
        # Insert each ordered item into in_order table
        
        for item in order_items:
            db.execute("INSERT INTO in_order (placed_order_id, offer_id, menu_item_id, quantity, item_price) VALUES (?, ?, ?, ?, ?)",
                       order_id, int(item['offer_id']), (int)(item['item_id']), item['quantity'], item['offer_price'])
                       

        # After a successful order insertion, redirect to an order confirmation page
        return redirect(url_for('order_confirmation_offer', order_id=order_id))

    except Exception as e:
        print(f"An error occurred: {e}")
        flash("An error occurred while placing the order.", "error")
        return redirect(url_for('home'))  # Redirect to a safe page if an error occurs

@app.route("/order_status/<int:order_id>")
@login_required
def order_status(order_id):
    # Get the current timestamp
    current_time = datetime.now()
    
    # Fetch status updates for the order that have occurred up until the current time
    status_updates = db.execute("""
        SELECT status, ts 
        FROM order_status 
        WHERE placed_order_id = ? AND ts <= ?
        ORDER BY ts ASC
    """, order_id, current_time)

    # Check if there are any status updates to display
    if not status_updates:
        flash("No status updates available for this order.")
        return redirect(url_for('order_history'))  # Redirect to the order history page.

    # Pass the status updates to the template
    return render_template("order_status.html", status_updates=status_updates, order_id=order_id)

@app.route("/order_confirmation/<int:order_id>")
@login_required
def order_confirmation(order_id):
    # Fetch the order details based on order_id
    order_details = db.execute("""
        SELECT po.order_time, po.estimated_delivery_time, po.delivery_address, 
               mio.quantity, mi.item_name, mi.price, (mio.quantity * mi.price) AS total_price
        FROM placed_order po
        JOIN in_order mio ON po.id = mio.placed_order_id
        JOIN menu_item mi ON mio.menu_item_id = mi.id
        WHERE po.id = ?
    """, order_id)
    

    # Calculate the total cost of the order
    total_cost = sum(item['total_price'] for item in order_details)

    # Fetch additional information if needed, like customer info or restaurant info
    # ...

    # Render the order confirmation page with the fetched details
    return render_template("order_confirmation.html", order_details=order_details, total_cost=total_cost, order_id=order_id)
@app.route("/order_confirmation_offer/<int:order_id>")
@login_required
def order_confirmation_offer(order_id):
    # Fetch the order details along with offer prices
    order_details = db.execute("""
        SELECT po.id as order_id, po.order_time, po.estimated_delivery_time, po.delivery_address, 
               mio.quantity, mi.item_name, mio.item_price, o.offer_price,
               (mio.quantity * o.offer_price) AS total_item_price
        FROM placed_order po
        JOIN in_order mio ON po.id = mio.placed_order_id
        JOIN menu_item mi ON mio.menu_item_id = mi.id
        JOIN in_offer io ON mi.id = io.menu_item_id
        JOIN offer o ON io.offer_id = o.id
        WHERE po.id = ?
    """, order_id)
    for item in order_details:
        print(item)
    # Sum the total_item_price to get the total cost of the order
    total_cost = sum(item['total_item_price'] for item in order_details)

    return render_template("order_confirmation_offer.html", order_details=order_details, total_cost=total_cost, order_id=order_id)


@app.route("/order_history")
@login_required
def order_history():
    customer_id = session["user_id"]  # Retrieve the logged-in customer's ID

    # Fetch the user's orders, including restaurant names and details about each order
    orders = db.execute("""
        SELECT po.id AS order_id, po.order_time, po.estimated_delivery_time, 
               po.delivery_address, po.final_price, r.name AS restaurant_name
        FROM placed_order po
        JOIN restaurant r ON po.Restaurant_r_id = r.r_id
        WHERE po.customer_id = ?
        ORDER BY po.order_time DESC
    """, customer_id)
    
    # Add an order number and item details to each order
    for index, order in enumerate(orders, start=1):
        order['order_number'] = index
        order['items'] = []
        order_items = db.execute("""
            SELECT io.quantity, io.item_price, mi.item_name
            FROM in_order io
            JOIN menu_item mi ON io.menu_item_id = mi.id
            WHERE io.placed_order_id = ?
        """, order['order_id'])

        for item in order_items:
            order['items'].append(item)
            # Calculate the total price for the order if not already provided
            order['total_price'] = sum(item['quantity'] * item['item_price'] for item in order_items)

    return render_template("order_history.html", orders=orders)


@app.route("/comment_on_order/<int:order_id>", methods=["GET", "POST"])
@login_required
def comment_on_order(order_id):
    if request.method == "POST":
        comment_text = request.form.get('comment_text')
        is_complaint = request.form.get('is_complaint')
        is_praise = request.form.get('is_praise')
        rating = request.form.get('rating')
        ic = False
        ip = False
        if(is_complaint):
            ic = True
        if(is_praise):
            ip = True
        current_time = datetime.now()
        # Insert the comment into the database
        db.execute("""
            INSERT INTO comment (placed_order_id, comment_text, ts, is_complaint, is_praise, rating)
            VALUES (?, ?, ?, ?, ?, ?)
        """, order_id, comment_text, current_time, ic, ip, rating)

        flash('Your comment has been submitted!')
        return redirect(url_for('order_history'))

    # If GET request, display the form
    return render_template("submit_comment.html", order_id=order_id)
@app.route("/my_comments")
@login_required
def my_comments():
    user_id = user_c_id  # Use your session or database call to get the user ID

    # Fetch the user's comments along with the restaurant name and order's total price
    comments = db.execute("""
        SELECT c.id, c.placed_order_id, c.comment_text, c.ts, c.is_complaint, c.is_praise, c.rating,
               r.name AS restaurant_name, po.final_price AS price
        FROM comment c
        JOIN placed_order po ON c.placed_order_id = po.id
        JOIN restaurant r ON po.Restaurant_r_id = r.r_id
        WHERE po.customer_id = ?
        ORDER BY c.id
    """, user_id)

    # Pass the comments to the template
    return render_template("my_comments.html", comments=comments)


@app.route("/logout")
def logout():
    # Clear the entire session
    session.clear()
    return redirect(url_for('login'))


@app.route("/register", methods=["GET","POST"])
def register():
    """Register user"""
    if request.method == "POST":
        id = request.form.get("id")
        customer_name = request.form.get("name")
        address = request.form.get("address")
        contact_phone = request.form.get("phone")
        email = request.form.get("email")
        confirmation_code = request.form.get("code")
        password = request.form.get("password")
        c_password = request.form.get("confirmation")
        cash = 0
        time_joined = datetime.now()
        if not password or not c_password:
            return apology("Either field Password or Re-enter Password is blank")
        if password != c_password:
            return apology("The two passwords do not match")
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        try:
            db.execute("INSERT INTO customer (id,customer_name, address, contact_phone, email, confirmation_code, password, time_joined, cash) VALUES(?,?,?,?,?,?,?,?,?)", id, customer_name, address, contact_phone, email, confirmation_code, hash, time_joined, cash)
        except ValueError:
            return apology("ID you have entered already exists!")
        return render_template("login.html")
    else:
        return render_template("register.html")
    
@app.route("/changepwd", methods=["GET", "POST"])
@login_required
def changepwd():
    u4 = user_c_id
    if request.method == "POST":
        o_password = request.form.get("originalpwd")
        password = request.form.get("newpwd")
        c_password = request.form.get("confirmpwd")
        if not o_password:
            return apology("Enter original password!")
        if not password:
            return apology("Enter new password!")
        if not c_password:
            return apology("Re-enter new password!")
        if password == o_password:
            return apology("Old password and New password cannot be the same!")
        if password != c_password:
            return apology("Passwords do not match!")
        d = db.execute("SELECT * FROM customer WHERE id = ?", u4)
        if not check_password_hash(d[0]["password"],o_password):
            return apology("Incorrect old password!")
        else:
            db.execute("UPDATE customer SET password = ? WHERE id = ?", generate_password_hash(password), u4)
        return redirect("/login")
    else:
        return render_template("changepwd.html")
