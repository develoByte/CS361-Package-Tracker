import zmq
import SaveTrackingNumbers

def main():
    """Microservice using ZeroMQ."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")  # Bind to port 5555

    print("Microservice is running... Waiting for requests.")
    while True:
        # Wait for the next request
        message = socket.recv_json()
        print(f"Received request: {message}")
        response = SaveTrackingNumbers.process_request(message)
        socket.send_json(response)
        print(f"Sent response: {response}")


if __name__ == "__main__":
    main()
