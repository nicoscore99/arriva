#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import xml.etree.ElementTree as ET
import yaml
import time

# Add file to system path
import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class WeatherQueryEngine:
    def __init__(self):
        credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.yaml')

        # Read the API key from the YAML file
        with open(credentials_path, 'r') as file:
            config = yaml.safe_load(file)
            self.client_id = config['MeteoMeteoProductFreemium']['client_id']
            self.client_secret = config['MeteoMeteoProductFreemium']['client_secret']
            self.auth_url = config['MeteoMeteoProductFreemium']['auth_url']
            self.forecast_url = config['MeteoMeteoProductFreemium']['forecast_url']
        
        self.params = {
            'type': 'day'
        }

        self.access_token_timer = None
        self.access_token = None

        self.forecast_timer = None
        self.forecast = None

    def get_auth_token(self):
        """
        Get a new access token using OAuth client credentials.
        """
        
        auth_response = requests.get(
            self.auth_url,
            params={'grant_type': 'client_credentials'},
            auth=(self.client_id, self.client_secret)
        )
        
        auth_response.raise_for_status()

        self.access_token_timer = time.time()

        return auth_response.json().get('access_token')

    def get_weather_forecast(self, latitude, longitude):
        """
        Get weather forecast based on latitude and longitude.
        """

        # Check if the access token is expired or not (max 50 queries per day)
        if self.forecast_timer is not None and (time.time() - self.forecast_timer) < 1728:
            return self.forecast

        # Reset every 7 days
        if self.access_token_timer is None or (time.time() - self.access_token_timer) > 604800:
            self.access_token = self.get_auth_token()

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        forecast_url = f"{self.forecast_url}/{latitude:.4f},{longitude:.4f}"

        # print the request URL for debugging
        print(f"Requesting forecast from: {forecast_url}")
        print(f"Using access token: {self.access_token}")

        forecast_response = requests.get(forecast_url, headers=headers, params=self.params)

        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        self.forecast = forecast_data
        self.forecast_timer = time.time()

        return forecast_data
    

def main():
    print("Weather Query Engine Test")
    weather_query = WeatherQueryEngine()

    latitude = 47.4467
    longitude = 9.4050

    forecast_data = weather_query.get_weather_forecast(latitude, longitude)
    print("Forecast Data:", forecast_data)

if __name__ == "__main__":
    main()