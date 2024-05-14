import concurrent.futures
import datetime

import FlightFinderApp_JG.Constants
from FlightFinderApp_JG.DestinationManager import RyanairDestinations
from FlightFinderApp_JG.SessionManager import SessionManager
from FlightFinderApp_JG.__Parsers import parse_flight_results, parse_connecting_flight_results

ryanair_destinations = RyanairDestinations()

class RyanairFlights:
    def __init__(self):

        self._num_queries = 0
        self.session_manager = SessionManager()
        self.session = self.session_manager.get_session()

    def __get_flights(self, departure_airport_code,
                      destination_airport_code=None,
                      destination_country=None):

        params = {"departureAirportIataCode": departure_airport_code,
                  "outboundDepartureDateFrom": _outbound_flight_date - datetime.timedelta(days=_date_flexibility_in_days),
                  "outboundDepartureDateTo": _outbound_flight_date + datetime.timedelta(days=_date_flexibility_in_days),
                  "priceValueTo": _price_value_to}

        if destination_country is not None:
            params["arrivalCountryCode"] = destination_country

        if destination_airport_code is not None:
            params["arrivalAirportIataCode"] = destination_airport_code

        if not _is_return_trip:
            url = FlightFinderApp_JG.Constants.FARE_API_URL + "oneWayFares"
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                return parse_flight_results(response.json())
            except Exception as e:
                return e

        params["inboundDepartureDateTo"] = _inbound_flight_date + datetime.timedelta(days=_date_flexibility_in_days)
        params["inboundDepartureDateFrom"] = _inbound_flight_date - datetime.timedelta(days=_date_flexibility_in_days)
        url = FlightFinderApp_JG.Constants.FARE_API_URL + "roundTripFares"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return parse_flight_results(response.json(), return_trip=True)
        except Exception as e:
            return e

    def __temp_find_flight(self, departure_airport_code,
                           arrival_airport_code):
        result = self.__get_flights(departure_airport_code=departure_airport_code,
                                    destination_airport_code=arrival_airport_code)
        if result:
            return result

    def find_flights(self, departure_airport_code: str,
                     arrival_airport_code: str = None,
                     outbound_date=datetime.date.today(),
                     date_flexibility_in_days=2,
                     trip_duration_in_days = 7,
                     price_value_to=999,
                     is_return_trip=False):

        direct_destination = []

        global _outbound_flight_date
        global _inbound_flight_date
        global _date_flexibility_in_days
        global _price_value_to
        global _is_return_trip

        _outbound_flight_date = self.__formate_date(outbound_date)
        _inbound_flight_date = _outbound_flight_date \
                               + datetime.timedelta(days=trip_duration_in_days)
        _date_flexibility_in_days = date_flexibility_in_days
        _price_value_to = price_value_to
        _is_return_trip = is_return_trip

        if departure_airport_code in ryanair_destinations.get_active_airport_codes():
            for dest in ryanair_destinations.get_path_to_destination(departure_airport_code):
                direct_destination.append(dest["arrivalAirport"]["code"])

            if arrival_airport_code in direct_destination:

                flights = self.__get_flights(departure_airport_code=departure_airport_code,
                                             destination_airport_code=arrival_airport_code)
                if flights:
                    print("Found direct flight and here search result based on your search criteria:")
                else:
                    print("No direct flights found. Check you search criteria...")
                return flights
            elif arrival_airport_code is None or not arrival_airport_code:
                flights = self.__get_flights(departure_airport_code=departure_airport_code)
                if flights:
                    print("Found flight and here search result based on your search criteria:")
                else:
                    print("No direct flights found. Check you search criteria...")
                return flights

            elif arrival_airport_code in ryanair_destinations.get_active_airport_codes():
                flights = self.__find_connecting_flights(departure_airport_code=departure_airport_code,
                                                         arrival_airport_code=arrival_airport_code,
                                                         direct_destination_list=direct_destination)

                if flights:
                    print("Found connecting flights and here search result based on your search criteria:")
                else:
                    print("Neither direct neither connecting flights were found. Check you search criteria...")
                return flights
            else:
                print("Arrival airport code: %s is not found. Check airport IATA code." %(arrival_airport_code))
        else:
            print("Departure airport code: %s is not found. Check airport IATA code." %(departure_airport_code))

    def __formate_date(self, outbound_date):
        return datetime.datetime.strptime(outbound_date, "%Y-%m-%d").date()


    def __find_connecting_flights(self, departure_airport_code,
                                  arrival_airport_code,
                                  direct_destination_list):
        connecting_airports = []
        flights_to_connecting_airports = []
        flights_from_connecting_airports = []

        for dep in ryanair_destinations.get_path_to_destination(arrival_airport_code):
            connecting_airports.append(dep["arrivalAirport"]["code"])

        direct_dest_set = set(direct_destination_list)
        depart_arri_set = set(connecting_airports)

        if direct_dest_set & depart_arri_set:
            # TODO extract to a seperate function both concurrent calls
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_flight = {
                    executor.submit(self.__temp_find_flight,
                                    departure_airport_code,
                                    arrival_airport_code):
                        arrival_airport_code for arrival_airport_code in (direct_dest_set & depart_arri_set)}
                for future in concurrent.futures.as_completed(future_to_flight):
                    try:
                        flight_data = future.result()

                    # TODO introduce a new exception
                    except Exception as exc:
                        print(exc)
                    else:
                        if flight_data is not None:
                            flights_to_connecting_airports.extend(flight_data)

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_flight = {executor.submit(self.__temp_find_flight,
                                                    departure,
                                                    arrival_airport_code):
                                    departure for departure in (direct_dest_set & depart_arri_set)}
                for future in concurrent.futures.as_completed(future_to_flight):
                    try:
                        flight_data = future.result()
                    # TODO introduce a new exception
                    except Exception as exc:
                        print(exc)
                    else:
                        if flight_data is not None:
                            flights_from_connecting_airports.extend(flight_data)

            return parse_connecting_flight_results(flights_to_connecting_airports=flights_to_connecting_airports,
                                                   flights_from_connecting_airports=flights_from_connecting_airports)
        return

