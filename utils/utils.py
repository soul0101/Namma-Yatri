def fetch_address_from_coordinates(latitude, longitude):
    # Find best matching top 5 addresses from latitude, longitude
    return [
        {
            "title": "Umiam Hostel Rd",
            "description": "IIT Guwahati, Guwahati, Assam 781039",
            "latitude": 26.188865,
            "longitude": 91.701626
        },
        {
            "title": "Dihing Canteent",
            "description": "IIT Guwahati, Guwahati, Assam 781039",
            "latitude": 26.187507,
            "longitude": 91.700096
        },
        {
            "title": "Barak Hostel",
            "description": "IIT Guwahati, Guwahati, Assam 781039",
            "latitude": 26.187865,
            "longitude": 91.700096
        }
    ]

def fetch_address_from_text(text):
    # Find best matching top 5 addresses from input
    return [
        {
            "title": "Deb Building",
            "description": "Lakhtokia, Fancy Bazaar, Guwahati, Assam 781001",
            "latitude": 26.182866,
            "longitude": 91.740479
        },
        {
            "title": "Cotton University Rd",
            "description": "Cotton University Rd, Fancy Bazaar, Guwahati, Assam 781001",
            "latitude": 26.182679,
            "longitude": 91.740597
        },
        {
            "title": "Kamarpatty Rd",
            "description": "Kamarpatty, Fancy Bazaar, Guwahati, Assam 781001",
            "latitude": 26.182749,
            "longitude": 91.740533
        }
    ]

def get_price_estimate(pickup_location, drop_location):
    return 561.28, 21

def is_message_response(data):
    try:
        response = data['entry'][0]['changes'][0]['value']['messages'][0]
        return True
    except: 
        False

def is_authenticated(data):
    return True