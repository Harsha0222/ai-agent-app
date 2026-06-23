
from openai import OpenAI
from dotenv import load_dotenv
import requests
import yfinance as yf

load_dotenv()

# Ollama Client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

COMPANY_SYMBOLS = {
    "tesla": "TSLA",
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "amazon": "AMZN",
    "nvidia": "NVDA",
    "meta": "META",
    "facebook": "META",
    "ibm": "IBM",
    "netflix": "NFLX"
}


def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return f"🌦 Weather in {city.title()}: {response.text}"

        return "Weather service unavailable"

    except Exception as e:
        return str(e)


def get_stock_price(company):

    try:
        company = company.lower().strip()

        symbol = COMPANY_SYMBOLS.get(
            company,
            company.upper()
        )

        stock = yf.Ticker(symbol)

        info = stock.info

        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")
        market_cap = info.get("marketCap")

        if current_price is None:
            return f"No stock data found for {symbol}"

        return f"""
📈 Stock: {symbol}

💰 Current Price: ${current_price}

📊 Previous Close: ${previous_close}

🏢 Market Cap: {market_cap:,}
"""

    except Exception as e:
        return f"Error: {str(e)}"


def run_agent(user_query):

    query = user_query.lower()

    # Weather Queries
    if "weather" in query:

        city = query.replace("weather", "")
        city = city.replace("in", "")
        city = city.strip()

        answer = get_weather(city)

        return {
            "answer": answer,
            "logs": [
                f"🌦 Weather Tool Called ({city})"
            ]
        }

    # Stock Queries
    stock_words = [
        "stock",
        "share",
        "price"
    ]

    if any(word in query for word in stock_words):

        company = None

        for name in COMPANY_SYMBOLS.keys():

            if name in query:
                company = name
                break

        if company is None:
            return {
                "answer": "Please specify a company name.",
                "logs": []
            }

        answer = get_stock_price(company)

        return {
            "answer": answer,
            "logs": [
                f"📈 Stock Tool Called ({company})"
            ]
        }

    # Normal Chat
    response = client.chat.completions.create(
        model="qwen2.5",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "logs": [
            "🤖 Answered by Ollama"
        ]
    }