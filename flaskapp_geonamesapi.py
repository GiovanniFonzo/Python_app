from flask import Flask, jsonify, make_response
import requests
import csv
import io

app = Flask(__name__)

USERNAME = 'yourusername'

def fetch_countries():
    url = f'http://api.geonames.org/countryInfoJSON?username={USERNAME}'
    response = requests.get(url)
    data = response.json()
    
    if 'geonames' in data:
        return data['geonames']
    else:
        return []

def fetch_states_for_country(geoname_id):
    url = f'http://api.geonames.org/childrenJSON?geonameId={geoname_id}&username={USERNAME}'
    response = requests.get(url)
    data = response.json()
    
    if 'geonames' in data:
        return data['geonames']
    else:
        return []

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = fetch_countries()
    country_data = []
    
    for country in countries:
        country_name = country['countryName']
        country_code = country['countryCode']
        
        # Fetch states based on geonameId
        states = fetch_states_for_country(country['geonameId'])
        state_names = [state['name'] for state in states]
        
        for state in state_names:
            country_data.append({
                'state': state,
                'country': country_name,
                'code': country_code
            })
    
    return jsonify(country_data)

@app.route('/export_csv', methods=['GET'])
def export_csv():
    # Fetch all country and state data
    countries = fetch_countries()
    
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['State/Province', 'Country', 'Country Code'])

    for country in countries:
        country_name = country['countryName']
        country_code = country['countryCode']
        
        # Fetch states for the country
        states = fetch_states_for_country(country['geonameId'])
        state_names = [state['name'] for state in states]

        # Write each state/country combination to the CSV
        for state in state_names:
            writer.writerow([state, country_name, country_code])

    # Prepare response
    output.seek(0)  # Rewind the StringIO object
    return make_response(output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=country_state_data.csv'
    })

if __name__ == '__main__':
    app.run(debug=True)

