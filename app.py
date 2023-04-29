import utils.utils as utils
from flask import Flask, request, jsonify, session
from state_machine.states.states import StartState
from state_machine.message_handler import Handler
app = Flask(__name__)

handler = None
state = None
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    global handler
    global state

    if request.method == 'GET':
        # Extract the verify token and challenge code from the query parameters
        verify_token = request.args.get('hub.verify_token')
        challenge_code = request.args.get('hub.challenge')

        print(verify_token, challenge_code)
        # Check that the verify token matches the one you provided in the WhatsApp Business Manager
        if verify_token == 'abc':
            # Return the challenge code to verify the webhook URL
            return challenge_code, 200
        else:
            # Return an error if the verify token is invalid
            return 'Invalid verify token', 403

    elif request.method == 'POST':
        # Handle incoming messages from WhatsApp here

        data = request.get_json()
        if utils.is_message_response(data):
            print("Incoming data: ", data)
            if handler is None:
                state = "START"
                phone_number_id = data['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
                wa_id = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                handler = Handler(phone_number_id, wa_id, StartState())

            handler.flow_handler(data)

        # Send the response back to the Meta WhatsApp API
        response = jsonify({'status': 'success'})
        return response, 200

if __name__ == '__main__':
    app.run(debug=True)