import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CMC_API_KEY = os.environ.get("CMC_API_KEY", "")
CMC_BASE = "https://pro-api.coinmarketcap.com/v2"


def cmc_get(path, params):
    resp = requests.get(
        CMC_BASE + path,
        params=params,
        headers={"X-CMC_PRO_API_KEY": CMC_API_KEY},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/gold")
def gold():
    try:
        data = cmc_get(
            "/cryptocurrency/quotes/latest",
            {"symbol": "XAU,XAUT", "convert": "USD"},
        )

        def extract(symbol):
            entries = data["data"].get(symbol)
            if not entries:
                return None
            item = entries[0]
            q = item["quote"]["USD"]
            return {
                "price": q["price"],
                "change_24h": q["percent_change_24h"],
                "change_7d": q["percent_change_7d"],
                "market_cap": q.get("market_cap"),
                "volume_24h": q.get("volume_24h"),
                "last_updated": q["last_updated"],
            }

        xau = extract("XAU")
        xaut = extract("XAUT")

        if not xau or not xaut:
            return jsonify({"error": "Missing symbol data from CMC"}), 502

        spread = xaut["price"] - xau["price"]
        spread_pct = (spread / xau["price"]) * 100

        return jsonify({
            "xau": xau,
            "xaut": xaut,
            "spread": {
                "usd": spread,
                "pct": spread_pct,
                "direction": "premium" if spread >= 0 else "discount",
            },
        })

    except requests.HTTPError as e:
        return jsonify({"error": f"CMC API error: {e.response.status_code}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
