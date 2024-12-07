import zmq
import pyperclip

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

print("Server started")

while True:
    tracking_info = socket.recv_string()

    pyperclip.copy(tracking_info)
    print("Tracking info copied to clipboard.")

    socket.send_string("Processed")
               