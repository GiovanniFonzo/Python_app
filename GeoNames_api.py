import requests

USERNAME = 'gifonz'

def fetch_countries():
    url = f'http://api.geonames.org/countryInfoJSON?username={USERNAME}'
    response = requests.get(url)
    data = response.json()

    # Check if 'geonames' exists in the response
    if 'geonames' in data:
        return data['geonames']
    else:
        # Print the error message if available
        if 'status' in data:
            print(f"Error: {data['status']['message']}")
        else:
            print("Unknown error occurred.")
        return []  # Return an empty list

def fetch_states_for_country(country_code):
    url = f'http://api.geonames.org/childrenJSON?geonameId={country_code}&username={USERNAME}'
    response = requests.get(url)
    data = response.json()

    # Check if 'geonames' exists in the response
    if 'geonames' in data:
        return data['geonames']
    else:
        # Print the error message if available
        if 'status' in data:
            print(f"Error: {data['status']['message']}")
        else:
            print("Unknown error occurred.")
        return []  # Return an empty list

def get_country_state_data():
    countries = fetch_countries()
    country_data = []
    
    for country in countries:
        country_name = country['countryName']
        country_code = country['countryCode']
        states = fetch_states_for_country(country['geonameId'])  # Replace with actual geonameId

        state_names = [state['name'] for state in states]  # Get state names if available
        country_data.append({
            'country': country_name,
            'code': country_code,
            'states': state_names
        })
    
    return country_data

# Call the function and print the data
country_state_data = get_country_state_data()
print(country_state_data)

