from flask import Flask, request, send_file, send_from_directory, jsonify
from medical_locator import get_medical_facilities, create_map
from geopy.geocoders import Nominatim
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('hackstrom frontend/index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if filename == 'medical_facilities_map.html':
        try:
            return send_file('medical_facilities_map.html')
        except Exception as e:
            logger.error(f"Error serving map file: {e}")
            return "Map not found", 404
    return send_from_directory('hackstrom frontend', filename)

@app.route('/find_medical_facilities', methods=['POST'])
def find_facilities():
    data = request.get_json()
    address = data.get('address')
    radius = data.get('radius', 5000)  # Default 5km radius
    
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    try:
        logger.info(f"Searching facilities near: {address}")
        
        # Initialize geocoder and get coordinates
        geolocator = Nominatim(user_agent="medical_locator")
        location = geolocator.geocode(address)
        
        if not location:
            logger.warning(f"Location not found for address: {address}")
            return jsonify({'error': 'Location not found'}), 404
            
        user_location = (location.latitude, location.longitude)
        logger.info(f"Found coordinates: {user_location}")
        
        # Get nearby facilities
        facilities = get_medical_facilities(user_location[0], user_location[1], radius)
        
        if not facilities:
            logger.warning(f"No facilities found near {address}")
            return jsonify({'error': 'No medical facilities found nearby'}), 404
            
        logger.info(f"Found {len(facilities)} facilities")
        
        # Create and save map
        m = create_map(user_location, facilities)
        output_file = 'medical_facilities_map.html'
        m.save(output_file)
        logger.info(f"Map saved to {output_file}")
        
        # Count facilities by type
        hospitals = sum(1 for f in facilities if f.tags.get('amenity') == 'hospital')
        pharmacies = sum(1 for f in facilities if f.tags.get('amenity') == 'pharmacy')
        
        return jsonify({
            'mapUrl': '/medical_facilities_map.html',
            'stats': {
                'hospitals': hospitals,
                'pharmacies': pharmacies,
                'total': len(facilities)
            },
            'location': {
                'address': location.address,
                'lat': location.latitude,
                'lon': location.longitude
            }
        })
        
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
