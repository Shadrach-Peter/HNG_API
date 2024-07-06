from flask import Flask, request
import requests, json, math

app = Flask(__name__)

@app.route('/api/hello/', methods=['GET'])
def home_page():
    # Capture the IP address from the request headers
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Print the user IP for debugging
    # print(f"User IP: {user_ip}")
    
    # Fetch geolocation data using the captured IP address
    API_KEY3 = 'a72ef5a91e35446680f114726240507'
    ip2_response = requests.get(f'http://api.weatherapi.com/v1/ip.json?key={API_KEY3}&q={user_ip}')
    main_IP = ip2_response.json()
    
    # Print the response from WeatherAPI for debugging
    # print(f"WeatherAPI response: {main_IP}")
    
    # Extract latitude and longitude from the response
    latitude = main_IP.get('lat', None)
    longitude = main_IP.get('lon', None)
    
    if latitude and longitude:
        # Fetch weather data using the obtained latitude and longitude
        API_KEY1 = '0e8314c999a24453aa1653a3f8055ce9'
        weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY1}')
        weather_data = weather_response.json()

        # Print the weather data response for debugging
        print(f"Weather data response: {weather_data}")
        
        temp_k = weather_data['main']['temp']
        resolve_temp_c = temp_k - 273.15  # Correct temperature conversion
        temp_c = math.trunc(resolve_temp_c)
        
        visitor_name = str(request.args.get('visitor_name'))
        data_set = {
            "client_ip": f"{user_ip}",
            "location": f"{main_IP['city']}",
            "greetings": f"Hello {visitor_name.title()}!, the temperature is {temp_c} degrees Celsius in {main_IP['city']}"
        }
        json_dump = json.dumps(data_set)
        return json_dump
    else:
        return json.dumps({"error": "Unable to retrieve geolocation data"}), 500

if __name__ == '__main__':
    app.run(port=9090)
