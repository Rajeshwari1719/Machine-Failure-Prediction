import requests
import pandas as pd

THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"
THINGSPEAK_API_KEY = "YOUR_READ_API_KEY"

def fetch_realtime_data(results=100):
    url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json"
    params = {
        "api_key": THINGSPEAK_API_KEY,
        "results": results
    }

    response = requests.get(url)
    data = response.json()["feeds"]

    df = pd.DataFrame(data)

    # Rename according to your fields
    df = df.rename(columns={
        "field1": "temperature",
        "field2": "vibration",
        "field3": "current"
    })

    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["vibration"] = pd.to_numeric(df["vibration"], errors="coerce")
    df["current"] = pd.to_numeric(df["current"], errors="coerce")

    return df.dropna()
