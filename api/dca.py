import json
import yfinance as yf

def handler(request):
    query = request.get("query", {})
    ticker = query.get("ticker", "AAPL")
    montant = float(query.get("montant", 100))
    start = query.get("start", "2000-01-01")

    data = yf.download(ticker, start=start)
    if data.empty:
        return { "status": 400, "body": json.dumps({"error": "invalid ticker"}) }

    close = data["Close"]
    shares = 0
    invested = 0

    for price in close:
        invested += montant
        shares += montant / price

    value = shares * close.iloc[-1]

    return {
        "status": 200,
        "body": json.dumps({
            "ticker": ticker,
            "invested": invested,
            "value": value
        })
    }
