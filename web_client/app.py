from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)

app.secret_key = 'somerandomsecretkey123'

# Set the base URL for the orchestrator service
BASE_URL = 'http://0.0.0.0:8000'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get the user's name from the JSON data
            data = request.get_json()
            user_name = data.get('name')

            # Ensure that a valid name is provided
            if not user_name:
                raise ValueError('Invalid or missing user name')

            # Send the user's name to the orchestrator's generate_user_id endpoint
            response = requests.post(f'{BASE_URL}/generateUserId', json={"name": user_name})

            if response.status_code == 200:
                # Successfully generated user ID
                user_data = response.json()
                session['user_id'] = user_data.get('user_id')  # Store user ID in session for future requests
                session['user_name'] = user_name  # Store user name in session
                return jsonify({'message': 'Registration successful', 'user_id': user_data.get('user_id')}), 200
            else:
                # Handle errors
                error_message = response.json().get('error', 'An error occurred during registration.')
                return jsonify({'error': error_message}), 500

        except Exception as e:
            # Handle unexpected errors
            return jsonify({'error': str(e)}), 500

    # Render the registration form for GET requests
    return render_template('register.html')

# Route for logging in and starting a session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            # Get the user's name from the JSON data
            data = request.get_json()
            user_name = data.get('name')

            # Ensure that a valid name is provided
            if not user_name:
                raise ValueError('Invalid or missing user name')

            # Send the user's name to the orchestrator's get_user_details endpoint
            response = requests.get(f'{BASE_URL}/getUserDetails/{user_name}')

            if response.status_code == 200:
                # User found, start the session
                user_data = response.json()
                session['user_id'] = user_data.get('user_id')
                session['user_name'] = user_data.get('user_name')
                return jsonify({'message': 'Login successful', 'user_id': user_data.get('user_id')}), 200
            else:
                # Handle errors
                error_message = response.json().get('error', 'An error occurred during registration.')
                return jsonify({'error': error_message}), 500

        except Exception as e:
            # Handle unexpected errors
            return jsonify({'error': str(e)}), 500

    # Return login render
    return render_template('login.html')


@app.route('/query', methods=['GET', 'POST'])
def query_weather():
    if request.method == 'POST':
        data = request.get_json()

        # Check if required fields are present in the request
        if 'location' not in data:
            return jsonify({'error': 'Incomplete data in the request'}), 400

        # Extract data from the request
        location = data['location']

        # Call the orchestrator's endpoint to get all weather details
        response = requests.get(f'{BASE_URL}/getAllWeatherDetails/{location}')

        try:
            if response.status_code == 200:
                # Successfully retrieved weather details
                all_weather_data = response.json().get('all_weather_data', {})

                print(all_weather_data)

                # Store the weather details in the session
                session['weather_details'] = all_weather_data

                # Render the weather.html template and pass weather_details
                return render_template('weather.html', weather_details=all_weather_data), 200

            else:
                # Handle errors
                error_message = response.json().get('error', 'An error occurred while retrieving weather details.')
                return jsonify({'error': error_message}), 500

        except ValueError as ve:
            # Handle JSON parsing errors
            return jsonify({'error': f"Error parsing JSON response: {ve}"}), 500

    # Render the query form for GET requests
    return render_template('query.html')

@app.route('/weather')
def weather():
    # Assuming you have weather details stored in the session
    weather_details = session.get('weather_details', {})

    return render_template('weather.html', weather_details=weather_details)


@app.route('/propose', methods=['GET', 'POST'])
def post_trip_proposal():
    if request.method == 'POST':
        try:
            # Get the required data from the JSON data
            data = request.get_json()
            # Get user_id and username from the session
            user_id = session.get('user_id')
            username = session.get('user_name')
            location = data.get('location')
            date = data.get('date')

            # Ensure that all required fields are present
            if not user_id or not username or not location or not date:
                return jsonify({'error': 'Incomplete data in the request'}), 400

            # Add user_id and username to the data before sending to the orchestrator
            data['user_id'] = user_id
            data['username'] = username

            # Send the data to the orchestrator's post_trip_proposal endpoint
            response = requests.post(f'{BASE_URL}/postTripProposal', json=data)

            if response.status_code == 200:
                # Trip proposal posted successfully
                trip_data = response.json()
                return jsonify({'message': 'Trip proposal posted successfully', 'trip_id': trip_data.get('trip_id')}), 200
            else:
                # Handle errors
                error_message = response.json().get('error', 'An error occurred during trip proposal posting.')
                return jsonify({'error': error_message}), 500

        except Exception as e:
            # Handle unexpected errors
            return jsonify({'error': str(e)}), 500

    return render_template('propose.html')


@app.route('/interest', methods=['GET'])
def get_all_trips():
    try:
        # Send a request to the orchestrator's endpoint to get all trip details
        response = requests.get(f'{BASE_URL}/getAllTrips')

        if response.status_code == 200:
            # Successfully retrieved trip details
            all_trip_details = response.json().get('trips', [])

            # Store the trip details in the session
            session['all_trip_details'] = all_trip_details

            return render_template('interest.html', trips=all_trip_details)
        else:
            # Handle errors
            error_message = response.json().get('error', 'An error occurred while retrieving trip details.')
            return jsonify({'error': error_message}), 500

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500


# Route for expressing interest in a trip
@app.route('/interest', methods=['POST'])
def express_interest():
    try:
        # Get user ID from the session
        user_id = session.get('user_id')

        # Get the trip details from the request data
        data = request.get_json()
        trip_id = data.get('trip_id')

        # Check if required fields are present
        if not user_id or not trip_id:
            return jsonify({'error': 'Incomplete data in the request'}), 400

        # Retrieve all trip details from the session
        all_trip_details = session.get('all_trip_details', [])

        # Find the selected trip details from the session data
        selected_trip = next((trip for trip in all_trip_details if trip['trip_id'] == trip_id), None)

        if not selected_trip:
            return jsonify({'error': 'Selected trip not found'}), 404

        # Add the liker_name field to the selected_trip
        selected_trip['liker_name'] = session.get('user_name')

        # Store the liked trip details in the user's session
        liked_trips = session.get('liked_trips', [])
        liked_trips.append(selected_trip)
        session['liked_trips'] = liked_trips

        print(session['liked_trips'])

        # Send the data to the orchestrator's expressInterest endpoint
        response = requests.post(f'{BASE_URL}/expressInterest', json={'user_id': user_id, 'trip_id': trip_id})

        if response.status_code == 200:
            # Interest expressed successfully
            return jsonify({'message': 'Interest expressed successfully'}), 200
        elif response.status_code == 404:
            # User or trip not found
            return jsonify({'error': 'User or trip not found'}), 404
        else:
            # Handle other errors
            error_message = response.json().get('error', 'An error occurred during interest expression.')
            return jsonify({'error': error_message}), 500

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500


# Route for displaying and managing liked trips
@app.route('/liked', methods=['GET', 'POST'])
def liked():
    try:
        # Check if the user is logged in

        if request.method == 'POST':
            # If it's a POST request, it means the user clicked the unlike button
            trip_id = request.form.get('trip_id')

            # Remove the trip from the liked_trips list in the session
            liked_trips = session.get('liked_trips', [])
            liked_trips = [trip for trip in liked_trips if trip['trip_id'] != trip_id]
            session['liked_trips'] = liked_trips

            return redirect(url_for('liked')), 200

        # Retrieve liked trips from the session
        liked_trips = session.get('liked_trips', [])

        return render_template('liked.html', liked_trips=liked_trips)

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        try:
            # Clear the user session
            session.pop('user_id', None)
            session.pop('user_name', None)

            # Clear the entire list of liked trips from the user's session, uncomment to run
            # session.pop('liked_trips', None)

            return render_template('home.html')

        except Exception as e:
            # Handle unexpected errors
            return jsonify({'error': str(e)}), 500

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=False, port=8080)


