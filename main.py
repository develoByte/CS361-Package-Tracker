# Package Tracker - Main Program
import zmq
import colorama
colorama.init(autoreset=True)

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
    print(colorama.Fore.CYAN + courier + " Tracking Number:")
    print(colorama.Fore.YELLOW + tracking_number)
    print()
    print(colorama.Fore.GREEN + "Name: " + colorama.Fore.RESET + "None")
    print(colorama.Fore.GREEN + "Status: " + colorama.Fore.RESET + status)
    print(colorama.Fore.GREEN + "Estimated Delivery: " + colorama.Fore.RESET + delivery_date)
    print("____________________________")

# Display Detailed Tracking Information
def display_detailed_tracking_info(tracking_info):
    for event in tracking_info['events']:
        print(colorama.Fore.CYAN + "Date: " + colorama.Fore.RESET + str(convert_datetime(event["occurrenceDatetime"])))
        print(colorama.Fore.CYAN + "Status: " + colorama.Fore.RESET + str(event["status"]))
        print(colorama.Fore.CYAN + "Location: " + colorama.Fore.RESET + str(event["location"]))
        print("____________________________")


# Save Tracking Number
def save_tracking_number(tracking_number, name):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    request = {"action": "save", "tracking_number": tracking_number, "name": name}
    socket.send_json(request)
    response = socket.recv_json()

    print(response)


# Get Saved Tracking Numbers
def get_saved_numbers():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    request = {"action": "retrieve"}
    socket.send_json(request)
    response = socket.recv_json()

    return response[0]["packages"]

# Display Saved Tracking Numbers
def choose_number(saved_numbers):
    print(colorama.Fore.CYAN + "\nSaved Tracking Numbers:")
    filtered_numbers = [package for package in saved_numbers if not package.get("archived", False)]
    for i, package in enumerate(filtered_numbers):
        print(colorama.Fore.YELLOW + str(i + 1) + ". " + colorama.Fore.GREEN + package["name"] + colorama.Fore.RESET + " (" + colorama.Fore.MAGENTA + package["tracking_number"] + colorama.Fore.RESET + ")")
    choice = input(colorama.Fore.CYAN + "\nPlease choose a tracking number (1-" + str(len(filtered_numbers)) + ")\nor enter a new tracking number: " + colorama.Fore.RESET)
    if choice.isdigit() and int(choice) <= len(filtered_numbers):
        return filtered_numbers[int(choice) - 1]["tracking_number"]
    else:
        return choice
    

# Archive Tracking Number
def archive_tracking_number(tracking_number):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    request = {"action": "archive", "tracking_number": tracking_number}
    socket.send_json(request)
    response = socket.recv_json()

# Share Tracking Number
def share_tracking_number(tracking_info, choice):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")
    request = {"tracking_info": str(tracking_info), "choice": "clipboard" if choice == "1" else "hastebin"}
    socket.send_json(request)
    response = socket.recv_string()
    print(response)


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
print(colorama.Fore.GREEN + "Welcome to Package Tracker!")
print(colorama.Fore.GREEN + "You may use this app to keep track of all your packages. We support over 1000 couriers worldwide, so you can track any package you want.")
tracking_number = input(colorama.Fore.CYAN + "\nPress enter to view saved tracking numbers or enter a new tracking number: ")

# If no tracking number is entered, allow user to choose from saved numbers
if tracking_number == "":
    numbers = get_saved_numbers()
    tracking_number = choose_number(numbers)

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
    print(colorama.Fore.CYAN + "\nOptions:")
    print(colorama.Fore.YELLOW + "1. Enter a New Tracking Number")
    print(colorama.Fore.YELLOW + "2. View Detailed Tracking Information")
    print(colorama.Fore.YELLOW + "3. Save Tracking Number")
    print(colorama.Fore.YELLOW + "4. Archive Tracking Number")
    print(colorama.Fore.YELLOW + "5. View Saved Tracking Numbers")
    print(colorama.Fore.YELLOW + "6. Share Tracking Number")
    print(colorama.Fore.YELLOW + "7. Exit")

    # User Input
    option = input(colorama.Fore.CYAN + "\nEnter your choice (1-6): ")

    if option == "1":
        track_package(input(colorama.Fore.CYAN + "\nPlease enter a new tracking number: "))
    elif option == "2":
        display_detailed_tracking_info(tracking_info)
    elif option == "3":
        save_tracking_number(tracking_number, input(colorama.Fore.CYAN + "\nPlease enter a name for this tracking number: "))
        print(colorama.Fore.GREEN + "\nTracking number saved successfully!")
    elif option == "4":
        #confirm user intent
        confirm = input(colorama.Fore.RED + "\nAre you sure you want to archive this tracking number? (y/n)")
        if confirm.lower() == "y" or confirm.lower() == "yes":
            archive_tracking_number(tracking_number)
            print(colorama.Fore.GREEN + "\nTracking number archived successfully!")
        else:
            print(colorama.Fore.GREEN + "\nTracking number not archived.")
    elif option == "5":
        numbers = get_saved_numbers()
        tracking_number = choose_number(numbers)
        track_package(tracking_number)
    elif option == "6":
        print(colorama.Fore.GREEN + "\nShare the tracking info with your friends!")
        # User chooses between copying info to clipboard or creating a HasteBin link
        print(colorama.Fore.CYAN + "\nOptions:")
        print(colorama.Fore.YELLOW + "1. Copy to Clipboard")
        print(colorama.Fore.YELLOW + "2. Create HasteBin Link")
        choice = input(colorama.Fore.CYAN + "\nEnter your choice (1-2): ")
        share_tracking_number(tracking_info, choice)

    elif option == "7":
        print(colorama.Fore.GREEN + "\nThank you for using Package Tracker!")
        exit()

while True:
    track_package(tracking_number)

    