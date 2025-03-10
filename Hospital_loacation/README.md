# Medical Facilities Locator

A Python application that helps users find nearby hospitals and medical shops (pharmacies) and displays them on an interactive map.

## Features

- Find hospitals and pharmacies near any location
- Interactive map visualization using Folium
- Color-coded markers:
  - 🔴 Red: Your location
  - 🟢 Green: Hospitals
  - 🔵 Blue: Pharmacies
- Customizable search radius
- Uses OpenStreetMap data for reliable worldwide coverage
- Displays facility names and types
- Automatically opens map in default web browser

## Requirements

- Python 3.x
- Required Python packages (installed automatically via requirements.txt):
  - folium==0.12.1 (for map visualization)
  - geopy==2.2.0 (for geocoding addresses)
  - overpy==0.6 (for accessing OpenStreetMap data)
  - requests==2.26.0 (for API requests)

## Installation

1. Clone or download this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the program:
```bash
python medical_locator.py
```

2. When prompted, enter:
   - Your address or location
   - Search radius in meters (default: 5000)

3. The program will:
   - Find your location coordinates
   - Search for nearby medical facilities
   - Create an interactive map
   - Open the map in your default web browser

## Map Features

The generated map (`medical_facilities_map.html`) shows:
- Your location marked with a red marker
- Hospitals marked with green markers
- Pharmacies marked with blue markers
- Clicking on markers shows:
  - Facility name
  - Facility type

## Technical Details

- Uses Nominatim geocoding service to convert addresses to coordinates
- Utilizes OpenStreetMap's Overpass API to find medical facilities
- Generates an HTML map using Folium library
- Map data is sourced from OpenStreetMap contributors

## Limitations

- Depends on OpenStreetMap data completeness
- Geocoding accuracy depends on the specificity of the input address
- Search results limited by Overpass API timeout (25 seconds)

## Contributing

Feel free to:
- Report issues
- Suggest features
- Submit pull requests

## License

This project is open source and available under the MIT License.
