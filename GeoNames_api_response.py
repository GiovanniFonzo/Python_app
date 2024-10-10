import requests

USERNAME = 'yourusername'

# Fetch countries from GeoNames API
def fetch_countries():
    url = f'http://api.geonames.org/countryInfoJSON?username={USERNAME}'
    response = requests.get(url)
    data = response.json()
    
    # Print the raw API response for debugging
    print("API Response:", data)
    
    return data['geonames']

# Fetch countries and print their names and codes
def get_country_state_data():
    countries = fetch_countries()
    country_data = []
    for country in countries:
        country_name = country['countryName']
        country_code = country['countryCode']
        country_data.append({'country': country_name, 'code': country_code})
    return country_data

# Call the function
country_state_data = get_country_state_data()
print(country_state_data)
