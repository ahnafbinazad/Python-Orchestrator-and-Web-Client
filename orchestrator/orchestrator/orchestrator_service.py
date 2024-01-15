from flask import Flask, jsonify, request
from models.user_model import User
from models.trip_model import Trip
from external_services.random_id_service import RandomIdService
from external_services.weather_forecast_service import WeatherForecastService
from tinydb import TinyDB, Query

app = Flask(__name__)

# Initialize the RandomIdService
random_id_service = RandomIdService()

# Initialize the WeatherForecastService
weather_service = WeatherForecastService()

# Initialize TinyDB for users and trips
db_users = TinyDB('database/db_users.json')
db_trips = TinyDB('database/db_trips.json')

# Initialize empty tables to store data
users_storage = db_users.table('users')
trips = db_trips.table('trips')

Query = Query()


@app.route('/')
def home():
    return 'Hello, this is the home page!'


# LOGIN AND SIGNUP methods
##########################

# Route for generating a unique user ID
@app.route('/generateUserId', methods=['POST'])
def generate_user_id():
    user_name = request.json.get('name')

    # Check if a user with the given name already exists
    existing_user = users_storage.search(Query.name == str(user_name))
    if existing_user:
        return jsonify({'error': 'User already exists with this name'}), 400

    # Generate a random user ID using an external service (random_id_service)
    user_id = random_id_service.generate_unique_id()

    # Create a User instance
    new_user = User(user_id, user_name)

    # Store the user in the TinyDB users table
    users_storage.insert({'user_id': new_user.user_id, 'name': new_user.name})

    return jsonify({'user_id': user_id}), 200


# Route for getting user details by user name
@app.route('/getUserDetails/<user_name>', methods=['GET'])
def get_user_details(user_name):
    # Search for the user with the given user name in the TinyDB 'users' table
    users = users_storage.search(Query.name == str(user_name))

    if users:
        # If user is found, return their details
        user = users[0]  # Assuming there's only one user with the given name
        return jsonify({'user_id': user.get('user_id'), 'user_name': user.get('name')}), 200
    else:
        # If user is not found, return an appropriate message
        return jsonify({'error': 'User not found'}), 500


# WEATHER DETAILS
##################

# Route for getting all weather details
@app.route('/getAllWeatherDetails/<location>', methods=['GET'])
def get_all_weather_details(location):
    try:
        all_weather_data = weather_service.get_all_weather_details(location)

        if isinstance(all_weather_data, dict):
            print(all_weather_data)
            return jsonify({'all_weather_data': all_weather_data}), 200
        else:
            return jsonify({'error': all_weather_data}), 500

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500


# POST TRIP PROPOSAL
####################

# Route for posting a trip proposal
@app.route('/postTripProposal', methods=['POST'])
def post_trip_proposal():
    data = request.get_json()

    # Check if required fields are present in the request
    if 'user_id' not in data or 'username' not in data or 'location' not in data or 'date' not in data:
        return jsonify({'error': 'Incomplete data in the request'}), 400

    # Extract data from the request
    user_id = data['user_id']
    username = data['username']
    location = data['location']
    date = data['date']

    # Check if a trip with the same location and date already exists
    existing_trip = trips.search((Query.location == str(location)) & (Query.date == date))
    if existing_trip:
        error = f"This trip has already been proposed."
        return jsonify({'error': error}), 400

    # Generate a random trip ID using the RandomIdService
    trip_id = random_id_service.generate_unique_id()

    # Get weather details using the WeatherForecastService
    weather_data = weather_service.get_weather_details(location)

    # Create a weather report string
    weather_report = f"{weather_data.get('weatherDesc', 'N/A')}, " \
                     f"Temperature: {weather_data.get('temp_C', 'N/A')}°C, " \
                     f"Feels like: {weather_data.get('feelsLikeC', 'N/A')}°C"

    print(weather_report)

    # Create a Trip instance
    new_trip = Trip(trip_id, user_id, username, location, date, weather_report)

    trips.insert({
        'trip_id': new_trip.trip_id,
        'user_id': new_trip.user_id,
        'username': new_trip.username,
        'location': new_trip.location,
        'date': new_trip.date,
        'weather': new_trip.weather
    })

    return jsonify({'message': 'Trip proposal posted successfully', 'trip_id': trip_id}), 200


# Expressing Interest
######################

# Route for getting all trip details
@app.route('/getAllTrips', methods=['GET'])
def get_all_trips():
    all_trip_details = []

    # Query all trips from the TinyDB 'trips' table
    all_trips = trips.all()

    for trip in all_trips:
        trip_details = {
            'trip_id': trip.get('trip_id'),
            'user_id': trip.get('user_id'),
            'username': trip.get('username'),
            'location': trip.get('location'),
            'date': trip.get('date'),
            'weather': trip.get('weather')
        }
        all_trip_details.append(trip_details)

    return jsonify({'trips': all_trip_details})


# Route for expressing interest in a trip
@app.route('/expressInterest', methods=['POST'])
def express_interest():
    data = request.get_json()

    # Check if required fields are present in the request
    if 'user_id' not in data or 'trip_id' not in data:
        return jsonify({'error': 'Incomplete data in the request'}), 400

    # Extract data from the request
    user_id = data['user_id']
    trip_id = data['trip_id']

    # Find the user with the given user ID in the TinyDB 'users' table
    users = users_storage.search(Query.user_id == int(user_id))
    trips_available = trips.search(Query.trip_id == int(trip_id))

    if users and trips_available:
        # Add the trip ID to the user's list of interested trips
        users_storage.update({'interested_trip_ids': int(trip_id)}, Query.user_id == int(user_id))

        return jsonify({'message': 'Interest expressed successfully'}), 200
    else:
        return jsonify({'error': 'User or trip not found'}), 404


if __name__ == '__main__':
    app.run(debug=False, port=8000)
