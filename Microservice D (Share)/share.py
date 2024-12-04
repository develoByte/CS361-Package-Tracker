import zmq
import json
import pyperclip
import requests

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

print("Server started")

while True:
    message = socket.recv()
    data = json.loads(message.decode())

    tracking_info = data.get('tracking_info', '')
    choice = data.get('choice', 'clipboard')

    

    if choice == 'clipboard':
        pyperclip.copy(tracking_info)
        print("Tracking info copied to clipboard.")
    elif choice == 'hastebin':
        response = requests.post('https://hastebin.com/documents', data=tracking_info)
        if response.status_code == 200:
            key = response.json()['key']
            url = f'https://hastebin.com/{key}'
            pyperclip.copy(url)
            print(f"Hastebin link copied to clipboard: {url}")
        else:
            print("Failed to upload to hastebin.")
    else:
        print("Invalid choice.")

    socket.send_string("Processed")
    # Format tracking info before processing
    if tracking_info:
        try:
            info = json.loads(tracking_info) if isinstance(tracking_info, str) else tracking_info
            formatted_output = f"Tracking Number: {info['trackingNumber']}\n"
            formatted_output += f"Status: {info['statusCategory'].title()} - {info['statusMilestone'].title()}\n"
            formatted_output += f"Estimated Delivery: {info['estimatedDeliveryDate'].split('T')[0]}\n\n"
            formatted_output += "Tracking History:\n"
            formatted_output += "-" * 50 + "\n"
            
            for event in info['events']:
                date = event['occurrenceDatetime'].replace('T', ' ').replace('Z', '')
                status = event['status']
                location = event['location'] if event['location'] else 'N/A'
                formatted_output += f"Time: {date}\n"
                formatted_output += f"Status: {status}\n"
                formatted_output += f"Location: {location}\n"
                formatted_output += "-" * 50 + "\n"
            
            tracking_info = formatted_output
        except Exception as e:
            print(f"Error formatting tracking info: {e}")