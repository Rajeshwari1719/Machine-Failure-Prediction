import requests
import pandas as pd

CHANNEL_ID = "3225416"
READ_API_KEY = "HAQ25PJNNX3R0JCR"

def fetch_realtime_data(field_num=1, results=200):
    url = (
        f"https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/"
        f"{field_num}.json?api_key={READ_API_KEY}&results={results}"
    )

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return pd.DataFrame()

        json_data = response.json()

        # ✅ SAFE CHECK (NO KeyError possible)
        feeds = json_data.get("feeds", [])
        if not feeds:
            return pd.DataFrame()

        rows = []
        for item in feeds:
            value = item.get(f"field{field_num}")
            if value is not None:
                rows.append({
                    "Time": item["created_at"],
                    "Sensor Value": float(value)
                })

        return pd.DataFrame(rows)

    except Exception:
        return pd.DataFrame()
