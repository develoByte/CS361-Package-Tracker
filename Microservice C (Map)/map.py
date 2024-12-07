import requests
from PIL import Image
from io import BytesIO
import zmq


def get_static_map(city, api_key, zoom=10, size="600x400", maptype="roadmap"):
    """
    Downloads a static map image from Google Maps Static API.

    :param city: City name or address (e.g., "Los Angeles, CA")
    :param api_key: Google Maps API key
    :param zoom: Zoom level (default is 12)
    :param size: Image size (e.g., "600x400")
    :param maptype: Map type (e.g., "roadmap", "satellite", "hybrid", "terrain")
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": city,
        "zoom": zoom,
        "size": size,
        "maptype": maptype,
        "key": api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        # Open and display the map
        image = Image.open(BytesIO(response.content))
        image.show()
    else:
        print(f"Error: Unable to fetch map (HTTP {response.status_code}).")
        print(response.json())  # Print error details if any

if __name__ == "__main__":
    API_KEY = "AIzaSyD104_6D7Iv3mFZ9IDLxC667o0ZiijMNsQ"
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5558")

    print("Server started")

    while True:
        city_name = socket.recv_string()
        print(f"Received request for {city_name}")

        get_static_map(city_name, API_KEY)
        socket.send_string("Processed")