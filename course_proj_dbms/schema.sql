CREATE TABLE IF NOT EXISTS restaurant (
            r_id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            cuisineType VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL);
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

        CREATE TABLE IF NOT EXISTS offer (
            id INTEGER PRIMARY KEY,
            date_active_from DATE NOT NULL,
            time_active_from TIME NOT NULL,
            date_active_to DATE NOT NULL,
            time_active_to TIME NOT NULL,
            offer_price DECIMAL(12, 2)
        );
        CREATE TABLE IF NOT EXISTS menu_item (
            id INTEGER PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            price DECIMAL(12, 2) NOT NULL,
            active BOOLEAN,
            Restaurant_r_id INTEGER,
            FOREIGN KEY (Restaurant_r_id) REFERENCES restaurant(r_id)
        );
        CREATE TABLE IF NOT EXISTS order_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placed_order_id INTEGER NOT NULL,
            status VARCHAR(255) NOT NULL,
            ts TIMESTAMP NOT NULL,
            FOREIGN KEY (placed_order_id) REFERENCES placed_order(id)
        );
        CREATE TABLE IF NOT EXISTS in_offer (
            id INTEGER PRIMARY KEY,
            offer_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            FOREIGN KEY (offer_id) REFERENCES offer(id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
        );
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
