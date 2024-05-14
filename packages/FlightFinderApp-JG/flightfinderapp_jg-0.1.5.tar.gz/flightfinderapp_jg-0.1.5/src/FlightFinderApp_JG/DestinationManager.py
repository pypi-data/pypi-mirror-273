import collections
import json
import time

import FlightFinderApp_JG.Constants
from FlightFinderApp_JG.SessionManager import SessionManager


class RyanairException(Exception):
    def __init__(self, message):
        super().__init__(f"Ryanair API: {message}")

class RyanairDestinations:

    def __init__(self):

        self._num_queries = 0
        self.session_manager = SessionManager()
        self.session = self.session_manager.get_session()
        self.active_airports = self.get_active_airports()

    def get_path_to_destination(self, departure_airport_code:str, queue=None):
        query = FlightFinderApp_JG.Constants.LOCATION_VIEW + departure_airport_code
        if queue is not None:
            return self.get_multi_response(query, departure_airport_code, queue)
        return self.get_response(query)

    def get_multi_response(self, query, code, queue):
        time.sleep(0.5)
        try:
            response = self.session.get(query)
            response.raise_for_status()
            return queue.put({code:json.loads(response.text)})
        except Exception as e:
            return e

    def get_response(self, query):
        try:
            response = self.session.get(query)
            response.raise_for_status()
            return json.loads(response.text)
        except RyanairException as e:
            return e

    # Returns all active airports and all information about hose where Ryanair operates
    def get_active_airports(self):
        query = FlightFinderApp_JG.Constants.ACTIVE_AIRPORT_VIEW
        try:
            response = self.session.get(query)
            response.raise_for_status()
            return json.loads(response.text)
        except RyanairException as e:
            return e
        #return json.loads(self.get_response(query).text)

    def get_active_airport_codes(self):
        active_airport_codes = []

        if self.active_airports is not None:
            for item in self.active_airports:
                active_airport_codes.append(item["code"])

        return active_airport_codes

    # Returns a list of airport name and IATA code for the specified city
    def get_active_airport_codes_by_city(self, city):
        cityAirports = {}

        for item in self.active_airports:
            if item['city']['name'] == city:
                cityAirports[item['name']] = item['code']
        if len(cityAirports) == 0:
            return 'No found active airports in specified city'

        return cityAirports

    def get_active_airports_by_country(self, country):
        country_airports = collections.defaultdict(list)

        for item in self.active_airports:
            if item['country']['name'] == country:

                temp_airport = {}
                temp_city = item['city']['name']
                temp_airport[item['name']] = item['code']
                if item['city']['name'] not in country_airports.keys():
                    country_airports[temp_city] = [temp_airport]
                elif not any(i.get(item['name']) == item['code'] for i in country_airports[temp_city]):
                    country_airports[temp_city].append(temp_airport)

        return country_airports

