from messenger.messenger import Messenger

class Handler():
    _state = None
    
    def __init__(self, phone_number_id, wa_id, state):
        print("HANDLER INITIALIZED ", phone_number_id, wa_id, state)
        self.phone_number_id = phone_number_id
        self.wa_id = wa_id
        self.pickup_locations_array = None
        self.drop_locations_array = None
        self.messenger = Messenger(phone_number_id, wa_id)
        self.price_estimate = None
        self.travel_distance = None
        self.setState(state)
        
    def setState(self, state):
        print(f"Context: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def flow_handler(self, data):
        self._state.flow_handler(data)
