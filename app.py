from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Securely loaded from .env
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city):
    """Fetch weather data from OpenWeatherMap API"""
    
    if not API_KEY:
        print("❌ API Key not set in .env!")
        return {'success': False, 'error': 'API key not configured. Please check your .env file.'}
    
    print(f"🔍 Searching for weather in: {city}")
    print(f"🔑 Using API key: {API_KEY[:8]}...{API_KEY[-4:] if len(API_KEY) > 12 else 'SHORT_KEY'}")
    
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 0) / 1000,
                'description': data['weather'][0]['description'].title(),
                'weather_main': data['weather'][0]['main'].lower(),
                'icon': data['weather'][0]['icon'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return {'success': True, 'data': weather_info}
        
        elif response.status_code == 401:
            return {'success': False, 'error': 'Invalid API key or authentication failed'}
        elif response.status_code == 404:
            return {'success': False, 'error': f"City '{city}' not found. Please check the spelling."}
        elif response.status_code == 429:
            return {'success': False, 'error': 'API rate limit exceeded. Please try again later.'}
        else:
            error_msg = response.json().get('message', f'HTTP {response.status_code}')
            return {'success': False, 'error': f'API Error: {error_msg}'}
    
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Request timeout - please try again'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Connection error - check your internet connection'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'Request error: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}

def get_wind_direction(degrees):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(degrees / 22.5) % 16
    return directions[index]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get('city', '').strip()
    
    if not city:
        return jsonify({'success': False, 'error': 'Please enter a city name'})
    
    result = get_weather_data(city)
    
    if result['success']:
        result['data']['wind_direction_text'] = get_wind_direction(result['data']['wind_direction'])
    
    return jsonify(result)

@app.route('/test-api')
def test_api():
    try:
        result = get_weather_data('London')
        return jsonify({
            'api_key_set': bool(API_KEY),
            'api_key_length': len(API_KEY) if API_KEY else 0,
            'test_result': result
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'api_key_set': bool(API_KEY),
            'api_key_length': len(API_KEY) if API_KEY else 0
        })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
