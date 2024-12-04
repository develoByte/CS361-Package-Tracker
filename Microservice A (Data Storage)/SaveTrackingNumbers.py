import zmq
import json
import os

DATA_FILE = "packages.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
        json.dump({"packages": []}, file)


def load_packages():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_packages(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def process_request(request):
    action = request.get("action")
    response = {"status": "error", "message": "Invalid action"}

    data = load_packages()

    if action == "save":
        tracking_number = request.get("tracking_number")
        name = request.get("name", "Unnamed Package")
        if tracking_number:
            data["packages"].append({"tracking_number": tracking_number, "name": name, "archived": False})
            save_packages(data)
            response = {"status": "success", "message": "Package saved"}
    elif action == "archive":
        tracking_number = request.get("tracking_number")
        for package in data["packages"]:
            if package["tracking_number"] == tracking_number:
                package["archived"] = True
                save_packages(data)
                response = {"status": "success", "message": "Package archived"}
                break
    elif action == "retrieve":
        response = {"status": "success", "packages": data["packages"]}
    elif action == "shutdown":
        response = {"status": "success", "message": "Shutting down the microservice"}
        return response, True  # Signal to shut down

    return response, False  # Continue running


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # Bind to port 5555

    print("Microservice is running... Waiting for requests.")
    while True:
        message = socket.recv_json()
        print(f"Received request: {message}")
        response, should_shutdown = process_request(message)
        socket.send_json(response)
        print(f"Sent response: {response}")

        if should_shutdown:
            print("Shutting down the microservice...")
            break


if __name__ == "__main__":
    main()
