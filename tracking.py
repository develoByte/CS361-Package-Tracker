import requests
import zmq
import json
import datetime

API_KEY = 'apik_GxjiaXBDhz0MF7XIMAg3qIvFiTCOWj'
url = "https://api.ship24.com/public/v1/tracking/search"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json; charset=utf-8"
}


def get_tracking_info(tracking_number):

    payload = {
        "trackingNumber": tracking_number
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json().get("data", {}).get("trackings", [])[0]
    result = []

    # Extract tracking information
    tracking_info = {
        "trackingNumber": data.get("shipment", {}).get("trackingNumbers")[0].get("tn"),
        "statusCategory": data.get("shipment", {}).get("statusCategory"),
        "statusMilestone": data.get("shipment", {}).get("statusMilestone"),
        "estimatedDeliveryDate": data.get("shipment", {}).get("delivery", {}).get("estimatedDeliveryDate"),
        "events": []
    }

    # Extract event information
    for event in data.get("events", []):
        event_info = {
            "occurrenceDatetime": event.get("occurrenceDatetime"),
            "status": event.get("status"),
            "location": event.get("location"),
            "courierCode": event.get("courierCode"),
            "statusCode": event.get("statusCode"),
            "statusCategory": event.get("statusCategory"),
            "statusMilestone": event.get("statusMilestone")
        }
        tracking_info["events"].append(event_info)
    
    result.append(tracking_info)

    return result


# Server for accepting tracking numbers

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Server started")

while True:
    message = socket.recv_string()
    print(f"\nRecieved: {message}")
    print(datetime.datetime.now())
    result = get_tracking_info(message)
    
    print(json.dumps(result, indent=4))

    socket.send_json(result)


