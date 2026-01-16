import requests
import pandas as pd

CHANNEL_ID = "3225416"
READ_API_KEY = "HAQ25PJNNX3R0JCR"

def fetch_realtime_data(field_num=1, results=50):
    url = (
        f"https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/"
        f"{field_num}.json?api_key={READ_API_KEY}&results={results}"
    )

    try:
        response = requests.get(url, timeout=5)
        json_data = response.json()

        feeds = json_data.get("feeds", [])
        if not feeds:
            return pd.DataFrame()

        data = []
        for feed in feeds:
            field_value = feed.get(f"field{field_num}")
            if field_value is not None:
                data.append({
                    "timestamp": feed.get("created_at"),
                    "value": float(field_value)
                })

        return pd.DataFrame(data)

    except Exception as e:
        print("Fetch error:", e)
        return pd.DataFrame()
