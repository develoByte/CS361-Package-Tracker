# server.py

import io
import zmq
import pandas as pd

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Server started")

def process(message):
    try:
        data = pd.read_csv(io.StringIO(message))

        if 'aqi' not in data.columns:
            return {"error": "Column 'aqi' not found in data"}

        stats = {
            "total_count": int(data.shape[0]),
            "aqi_mean": float(data['aqi'].mean()),
            "aqi_mode": float(data['aqi'].mode().iloc[0]),
            "aqi_min": float(data['aqi'].min()),
            "aqi_max": float(data['aqi'].max()),
            "aqi_std": float(data['aqi'].std())
        }

        return stats
    except Exception as e:
        return {"Error": str(e)}

while True:
    message = socket.recv_string()
    print(f"\nReceived:\n{message}")

    stats = process(message)

    print(stats)
    print("\nReturning Stats")
    socket.send_json(stats)

