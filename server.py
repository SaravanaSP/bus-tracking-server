from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store the bus tracking data in memory
bus_data = {}

@app.route('/')
def home():
    return "Bus Tracking System - API is running!"

@app.route('/update_location', methods=['GET'])
def update_location():
    bus_number = request.args.get('bus')
    
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        speed = float(request.args.get('speed'))
        direction = request.args.get('direction')  # direction as string
    except (ValueError, TypeError):
        return jsonify({
            "error": "Invalid parameter format. Latitude, Longitude, Speed must be numbers. Direction must be a string."
        }), 400

    # Check if any parameter is missing
    if not all([bus_number, lat, lon, speed, direction]):
        return jsonify({
            "error": "Missing parameters",
            "bus": bus_number,
            "lat": lat,
            "lon": lon,
            "speed": speed,
            "direction": direction
        }), 400

    # Update the bus data
    bus_data[bus_number] = {
        'latitude': lat,
        'longitude': lon,
        'speed': speed,
        'direction': direction
    }

    print(f"Bus {bus_number} updated: lat={lat}, lon={lon}, speed={speed}, direction={direction}")

    return jsonify({
        "status": "success",
        "message": f"Bus {bus_number} location updated",
        "bus": bus_number,
        "lat": lat,
        "lon": lon,
        "speed": speed,
        "direction": direction
    }), 200

@app.route('/get_location', methods=['GET'])
def get_location():
    bus_number = request.args.get('bus')

    if bus_number and bus_number in bus_data:
        location = bus_data[bus_number]
        return jsonify({
            'lat': location['latitude'],
            'lon': location['longitude'],
            'speed': location['speed'],
            'direction': location['direction'],
            'bus': bus_number
        }), 200
    else:
        return jsonify({
            "error": f"Bus {bus_number} not found"
        }), 404

# Do not use app.run() when deploying on Render
# Gunicorn will handle running the server
