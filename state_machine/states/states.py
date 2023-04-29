from state_machine.state import State
from utils.utils import fetch_address_from_coordinates, fetch_address_from_text, get_price_estimate, is_authenticated

class StartState(State):
    def flow_handler(self, data):
        self.context.messenger.send_text_message("Welcome to the Namma-Yatri App!")
        if is_authenticated(data):
            self.context.messenger.send_choose_pickup_message()
            self.context.setState(EnterPickupLocationState())
        else:
            self.context.messenger.send_text_message("It seems that you are not authenticated, kindly follow this link and login/register on the platform!\nhttps://shorturl.at/psFSW")
class EnterPickupLocationState(State):
    def flow_handler(self, data):
        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
        except:
            print("Unknown Webhook")
            return

        if message['type'] == 'text':
            text = message['text']['body']
            self.context.pickup_locations_array = fetch_address_from_text(text)
            if self.context.pickup_locations_array is None:
                self.context.messenger.send_invalid_address_message()
                return          
        elif message['type'] == 'location':
            location = message['location']
            latitude = location['latitude']
            longitude = location['longitude']
            self.context.pickup_locations_array = fetch_address_from_coordinates(latitude, longitude)

            if self.context.pickup_locations_array is None:
                self.context.messenger.send_invalid_address_message()
                return          
        else:
            # Unkown Response
            self.context.messenger.send_invalid_response_message()
            return
        
        self.context.messenger.send_location_list_message(self.context.pickup_locations_array)
        self.context.setState(ChoosePickupLocationState())

class ChoosePickupLocationState(State):
    def flow_handler(self, data) -> None:
        try:
            response = data['entry'][0]['changes'][0]['value']['messages'][0]
            response_type = response['type']
        except:
            print("Invalid data")
            return

        if response_type == 'interactive':
            try: 
                response_id = int(response['interactive']['list_reply']['id'])
                # response_text = response['interactive']['list_reply']['text']
            except ValueError:
                self.context.messenger.send_invalid_response_message()
                return
        elif response_type == 'text':
            try: 
                response_id = int(response['text']['body'])
            except ValueError:
                self.context.messenger.send_invalid_response_message()
                return
        else:
            self.context.messenger.send_invalid_response_message()
            return

        if response_id < 1 or response_id > len(self.context.pickup_locations_array):
            self.context.messenger.send_invalid_response_message()
            return
        
        self.context.pickup_location = self.context.pickup_locations_array[response_id-1]

        self.context.messenger.show_location(self.context.pickup_location, type='pickup')
        self.context.messenger.send_choose_drop_message()
        self.context.setState(EnterDropLocationState())

class EnterDropLocationState(State):
    def flow_handler(self, data):
        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
        except:
            print("Unknown Webhook")
            return

        if message['type'] == 'text':
            text = message['text']['body']
            self.context.drop_locations_array = fetch_address_from_text(text)
            if self.context.drop_locations_array is None:
                self.context.messenger.send_invalid_address_message()
                return          
        elif message['type'] == 'location':
            location = message['location']
            latitude = location['latitude']
            longitude = location['longitude']
            self.context.drop_locations_array = fetch_address_from_coordinates(latitude, longitude)

            if self.context.drop_locations_array is None:
                self.context.messenger.send_invalid_address_message()
                return          
        else:
            # Unkown Response
            self.context.messenger.send_invalid_response_message()
            return
        
        self.context.messenger.send_location_list_message(self.context.drop_locations_array)
        self.context.setState(ChooseDropLocationState())

class ChooseDropLocationState(State):
    def flow_handler(self, data) -> None:
        try:
            response = data['entry'][0]['changes'][0]['value']['messages'][0]
            response_type = response['type']
        except:
            print("Invalid data")
            return

        if response_type == 'interactive':
            try: 
                response_id = int(response['interactive']['list_reply']['id'])
                # response_text = response['interactive']['list_reply']['text']
            except ValueError:
                self.context.messenger.send_invalid_response_message()
                return
        elif response_type == 'text':
            try: 
                response_id = int(response['text']['body'])
            except ValueError:
                self.context.messenger.send_invalid_response_message()
                return
        else:
            self.context.messenger.send_invalid_response_message()
            return

        if response_id < 1 or response_id > len(self.context.drop_locations_array):
            self.context.messenger.send_invalid_response_message()
            return
        
        self.context.drop_location = self.context.drop_locations_array[response_id-1]

        self.context.messenger.show_location(self.context.drop_location, type='drop')
        self.context.price_estimate, self.context.travel_distance = get_price_estimate(self.context.pickup_location, self.context.drop_location)
        self.context.messenger.send_confirmation_message(self.context.price_estimate, self.context.travel_distance)
        self.context.setState(ConfirmationState())

class ConfirmationState(State):
    def flow_handler(self, data) -> None:
        try:
            response = data['entry'][0]['changes'][0]['value']['messages'][0]
            response_type = response['type']
        except:
            print("Invalid Response")
            return

        if response_type == 'interactive':
            response_id = response['interactive']['button_reply']['id']
        elif response_type == 'text':
            response_id = response['text']['body']
        else:
            self.context.messenger.send_text_message("Invalid response, please try again!")
            return

        if response_id == "confirm":
            self.context.messenger.send_text_message("Searching for Rides near you...")
            self.context.messenger.send_text_message("Driver Confirmed!\nThe Ride details are:\nDriver Name: Chirag Hegde\nVehicle No.: NY00HE1234\nDriver Contact: 9988776655\nThank you for using Namma-Yatri!")
            self.context.setState(OngoingRideState())
        elif response_id == "cancel":
            self.context.messenger.send_text_message("Cancelling your request... \n Send us a message if you change your mind!")
            self.context.setState(StartState())
        else:
            self.context.messenger.send_text_message("Invalid response, please try again!")

class SearchingRideState(State):
    def flow_handler(self, data):
        pass

class OngoingRideState(State):
    def flow_handler(self, data) -> None:
        pass