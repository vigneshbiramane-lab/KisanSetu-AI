import sqlite3

DATABASE_NAME = "kisansetu.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    connection = get_connection()

    cursor = connection.cursor()


    # ======================================
    # CROPS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crops (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL UNIQUE

        )
    """)


    # ======================================
    # MARKETS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS markets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            location TEXT NOT NULL

        )
    """)


    # ======================================
    # MARKET PRICES TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_prices (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            crop_id INTEGER NOT NULL,

            market_id INTEGER NOT NULL,

            price REAL NOT NULL,

            date TEXT NOT NULL,

            FOREIGN KEY (crop_id)
                REFERENCES crops(id),

            FOREIGN KEY (market_id)
                REFERENCES markets(id)

        )
    """)


    # ======================================
    # PRODUCE LISTINGS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produce_listings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            crop TEXT NOT NULL,

            quantity REAL NOT NULL,

            expected_price REAL NOT NULL,

            location TEXT NOT NULL,

            contact TEXT NOT NULL,

            status TEXT DEFAULT 'Available',

            created_at TEXT NOT NULL

        )
    """)


    # ======================================
    # OFFERS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS offers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            listing_id INTEGER NOT NULL,

            buyer_name TEXT NOT NULL,

            offer_price REAL NOT NULL,

            status TEXT DEFAULT 'Pending',

            created_at TEXT NOT NULL,

            FOREIGN KEY (listing_id)
                REFERENCES produce_listings(id)

        )
    """)


    # ======================================
    # SAVE TABLES
    # ======================================

    connection.commit()

    connection.close()


# ==========================================
# INSERT SAMPLE DATA
# ==========================================

def insert_sample_data():

    connection = get_connection()

    cursor = connection.cursor()


    # ======================================
    # CROPS
    # ======================================

    crops = [

        ("Onion",),

        ("Tomato",),

        ("Potato",)

    ]


    cursor.executemany("""
        INSERT OR IGNORE INTO crops (name)

        VALUES (?)

    """, crops)


    # ======================================
    # MARKETS
    # ======================================

    markets = [

        ("Nashik Market", "Nashik"),

        ("Pune Market", "Pune"),

        ("Mumbai Market", "Mumbai")

    ]


    for market in markets:

        cursor.execute("""
            SELECT id

            FROM markets

            WHERE name = ?

        """, (market[0],))


        existing = cursor.fetchone()


        if existing is None:

            cursor.execute("""
                INSERT INTO markets
                (name, location)

                VALUES (?, ?)

            """, market)


    connection.commit()


    # ======================================
    # GET CROP IDs
    # ======================================

    cursor.execute("""
        SELECT id, name

        FROM crops
    """)


    crop_rows = cursor.fetchall()


    crop_ids = {

        row["name"]: row["id"]

        for row in crop_rows

    }


    # ======================================
    # GET MARKET IDs
    # ======================================

    cursor.execute("""
        SELECT id, name

        FROM markets
    """)


    market_rows = cursor.fetchall()


    market_ids = {

        row["name"]: row["id"]

        for row in market_rows

    }


    # ======================================
    # MARKET PRICE DATA
    # ======================================

    prices = [

        ("Onion", "Nashik Market", 2450),

        ("Onion", "Pune Market", 2580),

        ("Onion", "Mumbai Market", 2650),

        ("Tomato", "Nashik Market", 2200),

        ("Tomato", "Pune Market", 2800),

        ("Tomato", "Mumbai Market", 2950),

        ("Potato", "Nashik Market", 1800),

        ("Potato", "Pune Market", 2050),

        ("Potato", "Mumbai Market", 2200)

    ]


    from datetime import date

    today = date.today().isoformat()


    for crop, market, price in prices:

        cursor.execute("""
            SELECT id

            FROM market_prices

            WHERE crop_id = ?

            AND market_id = ?

            AND date = ?

        """, (

            crop_ids[crop],

            market_ids[market],

            today

        ))


        existing = cursor.fetchone()


        if existing is None:

            cursor.execute("""
                INSERT INTO market_prices

                (crop_id, market_id, price, date)

                VALUES (?, ?, ?, ?)

            """, (

                crop_ids[crop],

                market_ids[market],

                price,

                today

            ))


    connection.commit()

    connection.close()


# ==========================================
# RUN DATABASE SETUP
# ==========================================

if __name__ == "__main__":

    create_tables()

    insert_sample_data()


    print()

    print("===================================")

    print(" KisanSetu AI Database")

    print("===================================")

    print("Database created successfully!")

    print("Sample market data inserted!")

    print("Produce listings table ready!")

    print("Offers table ready!")

    print("===================================")