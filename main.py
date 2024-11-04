# Package Tracker - Main Program
import zmq

# Functions

# Display Courier Name
def get_courier(courier_code):
    if courier_code == "us-post": return "USPS"
    elif courier_code == "fedex": return "FedEx"
    elif courier_code == "ups": return "UPS"
    elif courier_code == "dhl": return "DHL"
    elif courier_code == "amazon": return "Amazon"
    else: return courier_code
    
# Simplify Datetimes
def convert_datetime(datetime_str):
    try:
        return datetime_str.split("T")[0] + " " + datetime_str.split("T")[1].split("+")[0]
    except:
        return datetime_str
    

# Display Tracking Information
def display_tracking_info(courier, tracking_number, status, delivery_date):
    print("\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    print(courier + " Tracking Number:")
    print(tracking_number)
    print()
    print("Name: " + "None")
    print("Status: " + status)
    print("Estimated Delivery: " + delivery_date)
    print("____________________________")

# Display Detailed Tracking Information
def display_detailed_tracking_info(tracking_info):
    for event in tracking_info['events']:
        print("Date: " + str(convert_datetime(event["occurrenceDatetime"])))
        print("Status: " + str(event["status"]))
        print("Location: " + str(event["location"]))
        print("____________________________")

# Begin Program

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print('''
 ____            _                      _____               _             
|  _ \ __ _  ___| | ____ _  __ _  ___  |_   _| __ __ _  ___| | _____ _ __ 
| |_) / _` |/ __| |/ / _` |/ _` |/ _ \   | || '__/ _` |/ __| |/ / _ \ '__|
|  __/ (_| | (__|   < (_| | (_| |  __/   | || | | (_| | (__|   <  __/ |   
|_|   \__,_|\___|_|\_\__,_|\__, |\___|   |_||_|  \__,_|\___|_|\_\___|_|   
                           |___/                                          
      
      ''')
print("Welcome to Package Tracker!")
print("You may use this app to keep track of all your packages. We support over 1000 couriers worldwide, so you can track any package you want.")
tracking_number = input("\nPlease enter a new tracking number: ")

def track_package(tracking_number):
    # Get tracking information
    message = tracking_number
    socket.send_string(message)
    result = socket.recv_json()
    tracking_info = result[0]

    # Organize tracking information
    courier = get_courier(tracking_info['events'][0]['courierCode'])
    status = str(tracking_info['statusMilestone']).upper()
    delivery_date = convert_datetime(str(tracking_info['estimatedDeliveryDate']))
    if status == "DELIVERED":
        delivery_date = convert_datetime(str(tracking_info['events'][0]['occurrenceDatetime']))

    # Display tracking information
    display_tracking_info(courier, tracking_number, status, delivery_date)

    # Display Options
    print("\nOptions:")
    print("1. Enter a New Tracking Number")
    print("2. View Detailed Tracking Information")
    print("3. Exit")

    # User Input
    option = input("\nEnter your choice (1-3): ")

    if option == "1":
        track_package(input("\nPlease enter a new tracking number: "))
    elif option == "2":
        display_detailed_tracking_info(tracking_info)
    elif option == "3":
        print("\nThank you for using Package Tracker!")
        exit()

while True:
    track_package(tracking_number)