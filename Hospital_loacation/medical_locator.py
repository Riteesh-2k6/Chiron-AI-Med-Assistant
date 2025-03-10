import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import overpy
import webbrowser
import html

def get_medical_facilities(lat, lon, radius=5000):
    api = overpy.Overpass()
    
    # Query for hospitals and pharmacies within the radius
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="pharmacy"](around:{radius},{lat},{lon});
      way["amenity"="pharmacy"](around:{radius},{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    """
    
    try:
        result = api.query(query)
        return result.nodes + result.ways
    except Exception as e:
        print(f"Error fetching facilities: {e}")
        return []

def create_map(user_location, facilities):
    # Create a map centered at the user's location
    m = folium.Map(location=user_location, zoom_start=14)
    
    # Add marker for user's location
    user_lat, user_lon = user_location
    folium.Marker(
        user_location,
        popup='Your Location',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Add markers for medical facilities
    for facility in facilities:
        if hasattr(facility, 'lat') and hasattr(facility, 'lon'):
            facility_type = facility.tags.get('amenity', 'unknown')
            name = facility.tags.get('name', facility_type.title())
            color = 'green' if facility_type == 'hospital' else 'blue'
            
            # Create directions link
            directions_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={facility.lat},{facility.lon}&travelmode=driving"
            popup_html = f"""
                {html.escape(name)}<br>
                Type: {facility_type.title()}<br>
                <a href="{directions_url}" target="_blank">Get Directions</a>
            """
            
            folium.Marker(
                [facility.lat, facility.lon],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=color, icon='plus')
            ).add_to(m)
    
    return m

def main():
    # Initialize geocoder
    geolocator = Nominatim(user_agent="medical_locator")
    
    # Get user's location
    while True:
        address = input("Enter your address: ")
        try:
            location = geolocator.geocode(address)
            if location:
                break
            print("Could not find the address. Please try again.")
        except Exception as e:
            print(f"Error: {e}\nPlease try again.")
    
    user_location = (location.latitude, location.longitude)
    print(f"\nFound your location: {location.address}")
    
    # Get search radius
    try:
        radius = int(input("Enter search radius in meters (default 5000): ") or 5000)
    except ValueError:
        radius = 5000
    
    print("\nSearching for nearby medical facilities...")
    facilities = get_medical_facilities(user_location[0], user_location[1], radius)
    
    if not facilities:
        print("No medical facilities found in the specified radius.")
        return
    
    # Create and save map
    m = create_map(user_location, facilities)
    output_file = 'medical_facilities_map.html'
    m.save(output_file)
    
    hospitals = sum(1 for f in facilities if f.tags.get('amenity') == 'hospital')
    pharmacies = sum(1 for f in facilities if f.tags.get('amenity') == 'pharmacy')
    
    print(f"\nFound {hospitals} hospitals and {pharmacies} pharmacies.")
    print(f"Map has been created as '{output_file}'")
    
    # Open the map in the default browser
    webbrowser.open(output_file)

if __name__ == "__main__":
    main()
