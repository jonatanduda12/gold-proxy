# gold-proxy

Lightweight Flask proxy for CoinMarketCap gold data (XAU spot + XAUT).
Solves CORS — the browser dashboard calls this, not CMC directly.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Liveness check |
| `GET /api/gold` | XAU + XAUT prices, spread, 24h change |

### Sample response `/api/gold`
```json
{
  "xau":  { "price": 3312.40, "change_24h": 0.42, "change_7d": 1.1, ... },
  "xaut": { "price": 3318.75, "change_24h": 0.38, "change_7d": 0.9, ... },
  "spread": { "usd": 6.35, "pct": 0.192, "direction": "premium" }
}
```

## Deploy to Railway

1. Push this folder to a GitHub repo (or use Railway CLI)
2. Create a new Railway project → "Deploy from GitHub repo"
3. Add environment variable: `CMC_API_KEY=your_key_here`
4. Railway auto-detects Python and runs the Procfile
5. Copy the generated Railway URL (e.g. `https://gold-proxy-production.up.railway.app`)

## Local dev

```bash
pip install -r requirements.txt
CMC_API_KEY=your_key python app.py
# → http://localhost:5000/api/gold
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CMC_API_KEY` | Yes | Your CoinMarketCap Pro API key |
| `PORT` | No | Port to bind (Railway sets this automatically) |
