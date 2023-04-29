import requests
import config 

MESSAGING_PRODUCT = "whatsapp"
RECIPIENT_TYPE = "individual"

class Messenger():
    def __init__(self, phone_number_id, wa_id):
        self.phone_number_id = phone_number_id
        self.wa_id = wa_id

    def send_request(self, data):
        url = f"{config.API_ENDPOINT}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {config.API_TOKEN}",
            "Content-Type": "application/json"
        }
        print("Sent: ", data)
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def create_message_data(self, type, message_body):
        return {
            "messaging_product": MESSAGING_PRODUCT,
            "recipient_type": RECIPIENT_TYPE,
            "to": self.wa_id,
            "type": type,
            type: message_body
        }

    def send_text_message(self, text, preview_url=False):
        message_body = {
            "preview_url": preview_url,
            "body": str(text)
        }
        data = self.create_message_data("text", message_body)
        self.send_request(data)

    def send_image_message_by_id(self, image_id, image_caption):
        message_body = {"id": image_id, "caption": image_caption}
        data = self.create_message_data("image", message_body)
        self.send_request(data)

    def send_image_message_by_link(self, image_link, image_caption):
        message_body = {"link": image_link, "caption": image_caption}
        data = self.create_message_data("image", message_body)
        self.send_request(data)

    def send_location_message(self, latitude, longitude, name, address):
        message_body = {"latitude": latitude, "longitude": longitude, "name": name, "address": address}
        data = self.create_message_data("location", message_body)
        self.send_request(data)

    def send_choose_pickup_message(self):
        self.send_text_message("📍 Pickup Location 📍\nYou can either manually enter an address or share your GPS location.")
        self.send_image_message_by_id(6134484483283308, "To send us your phone's location automatically, click 📎 and then click on Location.")

    def send_choose_drop_message(self):
        self.send_text_message("📍 Drop Location 📍\nYou can either manually enter an address or share your GPS location.")

    def send_location_list_message(self, locations_array):
        rows = []
        for i, location in enumerate(locations_array[:5]):
            row = {
                "id": str(i+1),
                "title": location['title'],
                "description": location['description']
            }
            rows.append(row)
        header = {"type": "text", "text": "Pick an Address"}
        body = {"text": "Please select an address from the list below:"}
        action = {"button": "Select", "sections": [{"title": "Top 5 Address Matches", "rows": rows}]}
        interactive_body = {"type": "list", "header": header, "body": body, "action": action}
        data = self.create_message_data("interactive", interactive_body)
        self.send_request(data)

    def send_confirmation_message(self, price_estimate, travel_distance):
        body = {"text": "The travel distance is {0} km.\nThe estimated price is: {1}. Confirm?".format(travel_distance, price_estimate)}
        confirm_button = {"type": "reply", "reply": {"id": "confirm", "title": "Confirm"}}
        cancel_button = {"type": "reply", "reply": {"id": "cancel", "title": "Cancel"}}
        action = {"buttons": [confirm_button, cancel_button]}
        interactive_body = {"type": "button", "body": body, "action": action}
        data = self.create_message_data("interactive", interactive_body)
        self.send_request(data)    

    def send_invalid_address_message(self):
        self.send_text_message("⚠️ Sorry, could not find the given address, please try again!")
    
    def send_invalid_response_message(self):
        self.send_text_message("⚠️ Invalid response, please try again!")

    def show_location(self, location, type=None):
        if type == 'drop':
            text = "The selected location is:\n{0}".format(location['description'])
        elif type == 'pickup':
            text = "The selected location is:\n{0}".format(location['description'])
        else:
            text = ""
        self.send_text_message(text)
        self.send_location_message(location['latitude'], location['longitude'], location['title'], location['description'])