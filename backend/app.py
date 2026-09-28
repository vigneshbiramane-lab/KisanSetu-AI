from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE_NAME = "kisansetu.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ==========================================
# CORS
# ==========================================

@app.after_request
def add_cors_headers(response):

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"

    return response


# ==========================================
# HOME / BACKEND STATUS
# ==========================================

@app.route("/")
def home():

    return jsonify({
        "message": "KisanSetu AI Backend is running!",
        "status": "success"
    })


# ==========================================
# MARKET PRICES
# ==========================================

@app.route("/api/markets")
def markets():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            crops.name AS crop,
            markets.location AS market,
            market_prices.price AS price,
            market_prices.date AS date
        FROM market_prices
        JOIN crops
            ON market_prices.crop_id = crops.id
        JOIN markets
            ON market_prices.market_id = markets.id
        ORDER BY crops.name, market_prices.price
    """)

    rows = cursor.fetchall()

    connection.close()

    market_data = []

    for row in rows:

        market_data.append({

            "crop": row["crop"],
            "market": row["market"],
            "price": row["price"],
            "date": row["date"]

        })

    return jsonify(market_data)


# ==========================================
# AI PRICE PREDICTION
# ==========================================

@app.route("/api/predict")
def predict_price():

    crop = request.args.get(
        "crop",
        "Onion"
    )

    crop = crop.capitalize()


    # Recent historical market prices
    historical_prices = {

        "Onion": [
            2200,
            2250,
            2300,
            2280,
            2350,
            2400,
            2450
        ],

        "Tomato": [
            2400,
            2500,
            2450,
            2600,
            2700,
            2800,
            2900
        ],

        "Potato": [
            1750,
            1800,
            1850,
            1900,
            1950,
            2050,
            2150
        ]

    }


    # Check crop
    if crop not in historical_prices:

        return jsonify({

            "status": "error",

            "message":
                "Crop not available for prediction."

        }), 400


    prices = historical_prices[crop]


    # ==========================================
    # BASIC CALCULATIONS
    # ==========================================

    average_price = (
        sum(prices) /
        len(prices)
    )


    first_price = prices[0]


    latest_price = prices[-1]


    # ==========================================
    # PRICE CHANGE
    # ==========================================

    price_change = (
        latest_price -
        first_price
    )


    trend_percentage = (
        price_change /
        first_price
    ) * 100


    # ==========================================
    # TREND
    # ==========================================

    if trend_percentage > 3:

        trend = "Rising"

    elif trend_percentage < -3:

        trend = "Falling"

    else:

        trend = "Stable"


    # ==========================================
    # AI PREDICTED PRICE
    # ==========================================

    predicted_price = (
        latest_price +
        (price_change * 0.5)
    )


    predicted_price = round(
        predicted_price
    )


    # ==========================================
    # CONFIDENCE
    # ==========================================

    if abs(trend_percentage) > 8:

        confidence = "High"

    elif abs(trend_percentage) > 3:

        confidence = "Medium"

    else:

        confidence = "Low"


    # ==========================================
    # FARMER RECOMMENDATION
    # ==========================================

    if trend == "Rising":

        if predicted_price > latest_price:

            recommendation = (
                "Wait for a better price"
            )

            recommendation_reason = (
                "The recent price trend is rising "
                "and the predicted price is higher "
                "than the current price."
            )

        else:

            recommendation = "Sell Now"

            recommendation_reason = (
                "The current market price is "
                "relatively strong."
            )


    elif trend == "Falling":

        recommendation = "Consider Selling Now"

        recommendation_reason = (
            "The recent price trend is falling. "
            "Waiting may result in a lower price."
        )


    else:

        recommendation = "Market is Stable"

        recommendation_reason = (
            "The recent price movement is relatively "
            "stable. Farmers can compare nearby markets "
            "before selling."
        )


    # ==========================================
    # RETURN AI RESULT
    # ==========================================

    return jsonify({

        "status": "success",

        "crop": crop,

        "current_price":
            latest_price,

        "average_price":
            round(average_price),

        "predicted_price":
            predicted_price,

        "trend":
            trend,

        "trend_percentage":
            round(
                trend_percentage,
                2
            ),

        "confidence":
            confidence,

        "recommendation":
            recommendation,

        "recommendation_reason":
            recommendation_reason,

        "historical_prices":
            prices,

        "message":
            "AI prediction based on recent "
            "historical price trend."

    })


# ==========================================
# CREATE PRODUCE LISTING
# ==========================================

@app.route(
    "/api/listings",
    methods=["POST"]
)
def create_listing():

    data = request.get_json()


    if not data:

        return jsonify({

            "status": "error",

            "message":
                "No data received."

        }), 400


    required_fields = [

        "crop",
        "quantity",
        "expected_price",
        "location",
        "contact"

    ]


    for field in required_fields:

        if field not in data:

            return jsonify({

                "status": "error",

                "message":
                    f"{field} is required."

            }), 400


    try:

        crop = data["crop"]

        quantity = float(
            data["quantity"]
        )

        expected_price = float(
            data["expected_price"]
        )

        location = data["location"]

        contact = data["contact"]


    except (ValueError, TypeError):

        return jsonify({

            "status": "error",

            "message":
                "Quantity and expected price "
                "must be numbers."

        }), 400


    connection = get_connection()

    cursor = connection.cursor()


    created_at = datetime.now().isoformat()


    cursor.execute("""

        INSERT INTO produce_listings

        (
            crop,
            quantity,
            expected_price,
            location,
            contact,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        crop,
        quantity,
        expected_price,
        location,
        contact,
        "Available",
        created_at

    ))


    listing_id = cursor.lastrowid


    connection.commit()

    connection.close()


    return jsonify({

        "status": "success",

        "message":
            "Produce listing created successfully.",

        "listing_id":
            listing_id,

        "listing": {

            "id":
                listing_id,

            "crop":
                crop,

            "quantity":
                quantity,

            "expected_price":
                expected_price,

            "location":
                location,

            "contact":
                contact,

            "status":
                "Available",

            "created_at":
                created_at

        }

    })


# ==========================================
# GET PRODUCE LISTINGS
# ==========================================

@app.route(
    "/api/listings",
    methods=["GET"]
)
def get_listings():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT
            id,
            crop,
            quantity,
            expected_price,
            location,
            contact,
            status,
            created_at

        FROM produce_listings

        ORDER BY id DESC

    """)


    rows = cursor.fetchall()

    connection.close()


    listings = []


    for row in rows:

        listings.append({

            "id":
                row["id"],

            "crop":
                row["crop"],

            "quantity":
                row["quantity"],

            "expected_price":
                row["expected_price"],

            "location":
                row["location"],

            "contact":
                row["contact"],

            "status":
                row["status"],

            "created_at":
                row["created_at"]

        })


    return jsonify({

        "status":
            "success",

        "listings":
            listings

    })


# ==========================================
# CREATE BUYER OFFER
# ==========================================

@app.route(
    "/api/offers",
    methods=["POST"]
)
def create_offer():

    data = request.get_json()


    if not data:

        return jsonify({

            "status": "error",

            "message":
                "No data received."

        }), 400


    required_fields = [

        "listing_id",
        "buyer_name",
        "offer_price"

    ]


    for field in required_fields:

        if field not in data:

            return jsonify({

                "status": "error",

                "message":
                    f"{field} is required."

            }), 400


    try:

        listing_id = int(
            data["listing_id"]
        )

        buyer_name = data[
            "buyer_name"
        ]

        offer_price = float(
            data["offer_price"]
        )


    except (ValueError, TypeError):

        return jsonify({

            "status": "error",

            "message":
                "Invalid offer data."

        }), 400


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT id

        FROM produce_listings

        WHERE id = ?

    """, (
        listing_id,
    ))


    listing = cursor.fetchone()


    if not listing:

        connection.close()

        return jsonify({

            "status": "error",

            "message":
                "Produce listing not found."

        }), 404


    created_at = datetime.now().isoformat()


    cursor.execute("""

        INSERT INTO offers

        (
            listing_id,
            buyer_name,
            offer_price,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)

    """, (

        listing_id,
        buyer_name,
        offer_price,
        "Pending",
        created_at

    ))


    offer_id = cursor.lastrowid


    connection.commit()

    connection.close()


    return jsonify({

        "status":
            "success",

        "message":
            "Offer submitted successfully.",

        "offer_id":
            offer_id,

        "offer": {

            "listing_id":
                listing_id,

            "buyer_name":
                buyer_name,

            "offer_price":
                offer_price,

            "status":
                "Pending",

            "created_at":
                created_at

        }

    })


# ==========================================
# GET BUYER OFFERS
# ==========================================

@app.route(
    "/api/offers",
    methods=["GET"]
)
def get_offers():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT

            offers.id AS offer_id,

            offers.listing_id AS listing_id,

            offers.buyer_name AS buyer_name,

            offers.offer_price AS offer_price,

            offers.status AS status,

            offers.created_at AS created_at,

            produce_listings.crop AS crop,

            produce_listings.quantity AS quantity,

            produce_listings.expected_price AS expected_price,

            produce_listings.location AS location

        FROM offers

        JOIN produce_listings

            ON offers.listing_id =
               produce_listings.id

        ORDER BY offers.id DESC

    """)


    rows = cursor.fetchall()

    connection.close()


    offers = []


    for row in rows:

        offers.append({

            "offer_id":
                row["offer_id"],

            "listing_id":
                row["listing_id"],

            "buyer_name":
                row["buyer_name"],

            "offer_price":
                row["offer_price"],

            "status":
                row["status"],

            "created_at":
                row["created_at"],

            "crop":
                row["crop"],

            "quantity":
                row["quantity"],

            "expected_price":
                row["expected_price"],

            "location":
                row["location"]

        })


    return jsonify({

        "offers":
            offers,

        "status":
            "success"

    })


# ==========================================
# ACCEPT / REJECT OFFER
# ==========================================

@app.route(
    "/api/offers/<int:offer_id>/status",
    methods=["POST"]
)
def update_offer_status(
    offer_id
):

    data = request.get_json()


    if not data or "status" not in data:

        return jsonify({

            "status": "error",

            "message":
                "Status is required."

        }), 400


    new_status = data["status"]


    if new_status not in [

        "Accepted",
        "Rejected"

    ]:

        return jsonify({

            "status": "error",

            "message":
                "Status must be Accepted "
                "or Rejected."

        }), 400


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT id, status

        FROM offers

        WHERE id = ?

    """, (
        offer_id,
    ))


    offer = cursor.fetchone()


    if not offer:

        connection.close()

        return jsonify({

            "status": "error",

            "message":
                "Offer not found."

        }), 404


    cursor.execute("""

        UPDATE offers

        SET status = ?

        WHERE id = ?

    """, (

        new_status,
        offer_id

    ))


    connection.commit()

    connection.close()


    return jsonify({

        "status":
            "success",

        "offer_id":
            offer_id,

        "new_status":
            new_status,

        "message":
            f"Offer {new_status.lower()} successfully."

    })


# ==========================================
# RUN SERVER
# ==========================================

# ==========================================
# DASHBOARD STATISTICS
# ==========================================

@app.route("/api/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    # Total produce listings
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM produce_listings
    """)

    total_listings = cursor.fetchone()["total"]


    # Total buyer offers
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM offers
    """)

    total_offers = cursor.fetchone()["total"]


    # Pending offers
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM offers
        WHERE status = 'Pending'
    """)

    pending_offers = cursor.fetchone()["total"]


    # Accepted offers
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM offers
        WHERE status = 'Accepted'
    """)

    accepted_offers = cursor.fetchone()["total"]


    connection.close()


    return jsonify({

        "status": "success",

        "produce_listings":
            total_listings,

        "buyer_offers":
            total_offers,

        "pending_offers":
            pending_offers,

        "accepted_offers":
            accepted_offers

    })


if __name__ == "__main__":

    app.run(
        debug=True
    )