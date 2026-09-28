// ==========================================
// KISANSETU AI - FRONTEND JAVASCRIPT
// ==========================================

const API_URL = "http://127.0.0.1:5000";


// ==========================================
// PAGE NAVIGATION
// ==========================================

function openBestMarket() {
    window.location.href = "pages/bestmarket.html";
}


function openPricePrediction() {
    window.location.href = "pages/priceprediction.html";
}


function openSellProduce() {
    window.location.href = "pages/sellproduce.html";
}


function openBuyerOffers() {
    window.location.href = "pages/buyeroffers.html";
}


function openFarmerOffers() {
    window.location.href = "pages/farmeroffers.html";
}


// ==========================================
// MARKET PRICES
// ==========================================

function openMarketPrices() {

    const marketSection =
        document.getElementById("market");

    if (marketSection) {

        marketSection.scrollIntoView({
            behavior: "smooth"
        });

    }

}


// ==========================================
// LOAD MARKET PRICES
// ==========================================

async function loadMarketPrices() {

    const priceGrid =
        document.getElementById("priceGrid");

    if (!priceGrid) {
        return;
    }

    priceGrid.innerHTML = `
        <div class="loading-message">
            <div style="font-size:32px;">⏳</div>
            <p>Loading latest market prices...</p>
        </div>
    `;

    try {

        const response =
            await fetch(`${API_URL}/api/markets`);

        if (!response.ok) {
            throw new Error("Market API failed");
        }

        const data =
            await response.json();

        if (!data || data.length === 0) {

            priceGrid.innerHTML = `
                <div class="loading-message">
                    <div style="font-size:32px;">📊</div>
                    <p>No market price data available.</p>
                </div>
            `;

            return;
        }


        const cropData = {};


        data.forEach(function(item) {

            const crop = item.crop;

            if (!cropData[crop]) {
                cropData[crop] = [];
            }

            cropData[crop].push(item);

        });


        const crops =
            Object.keys(cropData).slice(0, 3);


        let html = "";


        crops.forEach(function(crop) {

            const markets =
                cropData[crop];


            const bestMarket =
                markets.reduce(
                    function(best, current) {

                        return Number(current.price) >
                               Number(best.price)
                            ? current
                            : best;

                    }
                );


            const price =
                Number(bestMarket.price);


            let icon = "🌾";


            if (crop.toLowerCase() === "onion") {
                icon = "🧅";
            }

            else if (crop.toLowerCase() === "tomato") {
                icon = "🍅";
            }

            else if (crop.toLowerCase() === "potato") {
                icon = "🥔";
            }


            html += `

                <div class="price-card">

                    <div class="crop-icon">
                        ${icon}
                    </div>

                    <h3>
                        ${crop}
                    </h3>

                    <p>
                        ${bestMarket.market} Market
                    </p>

                    <strong class="price">
                        ₹${price.toLocaleString("en-IN")}
                    </strong>

                    <span>
                        / quintal
                    </span>

                    <div class="up">
                        Live Backend Data
                    </div>

                </div>

            `;

        });


        priceGrid.innerHTML = html;

    }


    catch (error) {

        console.error(
            "Market API error:",
            error
        );


        priceGrid.innerHTML = `

            <div class="loading-message">

                <div style="font-size:32px;">
                    ⚠️
                </div>

                <p>
                    Unable to connect to KisanSetu backend.
                </p>

                <small>
                    Make sure Python Flask server is running.
                </small>

            </div>

        `;

    }

}



// ==========================================
// LOAD DASHBOARD
// ==========================================

async function loadDashboard() {

    try {

        const response =
            await fetch(`${API_URL}/api/dashboard`);


        if (!response.ok) {
            throw new Error("Dashboard API failed");
        }


        const data =
            await response.json();


        const totalListings =
            document.getElementById("totalListings");

        const totalOffers =
            document.getElementById("totalOffers");

        const pendingOffers =
            document.getElementById("pendingOffers");

        const acceptedOffers =
            document.getElementById("acceptedOffers");


        if (totalListings) {
            totalListings.textContent =
                data.produce_listings;
        }


        if (totalOffers) {
            totalOffers.textContent =
                data.buyer_offers;
        }


        if (pendingOffers) {
            pendingOffers.textContent =
                data.pending_offers;
        }


        if (acceptedOffers) {
            acceptedOffers.textContent =
                data.accepted_offers;
        }


        const status =
            document.getElementById("dashboardStatus");


        if (status) {

            status.textContent =
                "🟢 Live database connected";

        }

    }


    catch (error) {

        console.error(
            "Dashboard API error:",
            error
        );


        const status =
            document.getElementById("dashboardStatus");


        if (status) {

            status.textContent =
                "🔴 Backend connection unavailable";

        }

    }

}



// ==========================================
// CHECK BACKEND
// ==========================================

async function checkBackend() {

    try {

        const response =
            await fetch(`${API_URL}/`);

        if (response.ok) {

            console.log(
                "✅ KisanSetu backend connected."
            );

        }

    }

    catch (error) {

        console.log(
            "⚠️ Backend is not running."
        );

    }

}



// ==========================================
// START APPLICATION
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        console.log(
            "🌾 KisanSetu AI frontend started."
        );


        checkBackend();

        loadMarketPrices();

        loadDashboard();

    }
);