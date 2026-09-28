// ==========================================
// KISANSETU AI - FRONTEND JAVASCRIPT
// ==========================================

const API_URL = "http://127.0.0.1:5000";


// ==========================================
// PAGE NAVIGATION
// ==========================================

function openBestMarket() {

    window.location.href =
        "pages/bestmarket.html";

}


function openPricePrediction() {

    window.location.href =
        "pages/priceprediction.html";

}


function openSellProduce() {

    window.location.href =
        "pages/sellproduce.html";

}


function openBuyerOffers() {

    window.location.href =
        "pages/buyeroffers.html";

}


// ==========================================
// MARKET PRICES BUTTON
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
// BUYER OFFERS
// KEEPING CURRENT HOMEPAGE BEHAVIOUR
// ==========================================

function showMessage(message) {

    alert(message + " feature will be connected next.");

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


    try {

        const response =
            await fetch(
                `${API_URL}/api/markets`
            );


        if (!response.ok) {

            throw new Error(
                "Backend response was not successful."
            );

        }


        const data =
            await response.json();


        console.log(
            "Market data received:",
            data
        );


        if (!data || data.length === 0) {

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


            if (
                crop.toLowerCase() === "onion"
            ) {

                icon = "🧅";

            }

            else if (
                crop.toLowerCase() === "tomato"
            ) {

                icon = "🍅";

            }

            else if (
                crop.toLowerCase() === "potato"
            ) {

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

                    <div class="price-row">

                        <strong class="price">
                            ₹${price.toLocaleString("en-IN")}
                        </strong>

                        <span>
                            / quintal
                        </span>

                    </div>

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

        /*
           Keep the original HTML cards visible
           if backend is unavailable.
        */

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
            "⚠️ KisanSetu backend is not running."
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

    }
);