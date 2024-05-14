import datetime
import json


def parse_flight_results(flight_data, return_trip=False):
    flights = []
    for item in flight_data["fares"]:
        data = {"outbound": {
            "departureCountry": item["outbound"]["departureAirport"]["countryName"],
            "departureCity": item["outbound"]["departureAirport"]["city"]["name"],
            "departureIATACode": item["outbound"]["departureAirport"]["iataCode"],
            "arrivalCountry": item["outbound"]["arrivalAirport"]["countryName"],
            "arrivalCity": item["outbound"]["arrivalAirport"]["city"]["name"],
            "arrivalIATACode": item["outbound"]["arrivalAirport"]["iataCode"],
            "departureDate": item["outbound"]["departureDate"],
            "arrivalDate": item["outbound"]["arrivalDate"],
            "price": item["outbound"]["price"]["value"],
            "currency": item["outbound"]["price"]["currencyCode"],
            "priceUpdatedOn": item["outbound"]["priceUpdated"]},
            "summary": {
                "price": item["summary"]["price"]["value"],
                "currency": item["summary"]["price"]["currencyCode"]
            }
        }
        if return_trip:
            data.update({"inbound": {
                "departureCountry": item["inbound"]["departureAirport"]["countryName"],
                "departureCity": item["inbound"]["departureAirport"]["city"]["name"],
                "departureIATACode": item["inbound"]["departureAirport"]["iataCode"],
                "arrivalCountry": item["inbound"]["arrivalAirport"]["countryName"],
                "arrivalCity": item["inbound"]["arrivalAirport"]["city"]["name"],
                "arrivalIATACode": item["inbound"]["arrivalAirport"]["iataCode"],
                "departureDate": item["inbound"]["departureDate"],
                "arrivalDate": item["inbound"]["arrivalDate"],
                "price": item["inbound"]["price"]["value"],
                "currency": item["inbound"]["price"]["currencyCode"],
                "priceUpdatedOn": item["inbound"]["priceUpdated"]},
                "summary": {
                    "price": item["summary"]["price"]["value"],
                    "currency": item["summary"]["price"]["currencyCode"],
                    "tripDuration": item["summary"]["tripDurationDays"]
                }})
        flights.append(json.dumps(data))

    return flights

def parse_connecting_flight_results(flights_to_connecting_airports, flights_from_connecting_airports):

    flight_data = []

    for item_to in flights_to_connecting_airports:
        flight_to = json.loads(item_to)

        for item_from in flights_from_connecting_airports:
            flight_from = json.loads(item_from)

            if flight_from["outbound"]["departureIATACode"] == flight_to["outbound"]["arrivalIATACode"] and \
                    (datetime.datetime.strptime(flight_from["outbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")
                    - datetime.datetime.strptime(flight_to["outbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S")).days > 0 and \
                    "inbound" in flight_from and \
                    (datetime.datetime.strptime(flight_to["inbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")
                     - datetime.datetime.strptime(flight_from["inbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S")).days > 0:

                data = {"outbound": {
                    "toConnecting":{
                        "departureCity": flight_to["outbound"]["departureCity"],
                        "departureIataCode": flight_to["outbound"]["departureIATACode"],
                        "arrivalCity": flight_to["outbound"]["arrivalCity"],
                        "arrivalIataCode": flight_to["outbound"]["arrivalIATACode"],
                        "departureDate": flight_to["outbound"]["departureDate"],
                        "arrivalDate": flight_to["outbound"]["arrivalDate"],
                        "price": flight_to["outbound"]["price"],
                        "currency": flight_to["outbound"]["currency"],
                        "priceUpdatedOn": flight_to["outbound"]["priceUpdatedOn"]},
                    "fromConnecting": {
                        "departureCity": flight_from["outbound"]["departureCity"],
                        "departureIataCode": flight_from["outbound"]["departureIATACode"],
                        "arrivalCity": flight_from["outbound"]["arrivalCity"],
                        "arrivalIataCode": flight_from["outbound"]["arrivalIATACode"],
                        "departureDate": flight_from["outbound"]["departureDate"],
                        "arrivalDate": flight_from["outbound"]["arrivalDate"],
                        "price": flight_from["outbound"]["price"],
                        "currency": flight_from["outbound"]["currency"],
                        "priceUpdatedOn": flight_from["outbound"]["priceUpdatedOn"]},
                        "summary": {
                            "timeBetweenFlights": str(
                                datetime.datetime.strptime(flight_from["outbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")
                                - datetime.datetime.strptime(flight_to["outbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S"))
                        }
                    },}
                for item_back in flights_to_connecting_airports:
                    flight_back = json.loads(item_back)
                    if flight_back["inbound"]["departureIATACode"] == flight_from["inbound"]["arrivalIATACode"]:

                        data.update({"inbound": {
                        "toConnecting":{
                            "departureCity": flight_from["inbound"]["departureCity"],
                            "departureIataCode": flight_from["inbound"]["departureIATACode"],
                            "arrivalCity": flight_from["inbound"]["arrivalCity"],
                            "arrivalIataCode": flight_from["inbound"]["arrivalIATACode"],
                            "departureDate": flight_from["inbound"]["departureDate"],
                            "arrivalDate": flight_from["inbound"]["arrivalDate"],
                            "price": flight_from["inbound"]["price"],
                            "currency": flight_from["inbound"]["currency"],
                            "priceUpdatedOn": flight_from["inbound"]["priceUpdatedOn"]},
                        "fromConnecting": {
                            "departureCity": flight_back["inbound"]["departureCity"],
                            "departureIataCode": flight_back["inbound"]["departureIATACode"],
                            "arrivalCity": flight_back["inbound"]["arrivalCity"],
                            "arrivalIataCode": flight_back["inbound"]["arrivalIATACode"],
                            "departureDate": flight_back["inbound"]["departureDate"],
                            "arrivalDate": flight_back["inbound"]["arrivalDate"],
                            "price": flight_back["inbound"]["price"],
                            "currency": flight_back["inbound"]["currency"],
                            "priceUpdatedOn": flight_back["inbound"]["priceUpdatedOn"]},
                        "summary": {
                            "timeBetweenFlights": str(
                                    datetime.datetime.strptime(flight_back["inbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")
                                    - datetime.datetime.strptime(flight_from["inbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S"))
                            }},
                        "tripSummary":{
                            "totalPrice": str(round(flight_to["outbound"]["price"]
                                                   +flight_from["outbound"]["price"]
                                                   +flight_from["inbound"]["price"]
                                                   +flight_back["inbound"]["price"], 2)),
                            "tripDuration": str(
                                datetime.datetime.strptime(flight_back["inbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S")
                                - datetime.datetime.strptime(flight_to["outbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")),
                            "timeInDestination": str(
                                datetime.datetime.strptime(flight_from["inbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")
                                - datetime.datetime.strptime(flight_from["outbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S"))
                        }})

                        flight_data.append(json.dumps(data))

            elif flight_from["outbound"]["departureIATACode"] == flight_to["outbound"]["arrivalIATACode"] and \
                    "inbound" not in flight_from and (datetime.datetime.strptime(flight_from["outbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")
                     - datetime.datetime.strptime(flight_to["outbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S")).days > 0:

                data = {"outbound": {
                    "toConnecting":{
                        "departureCity": flight_to["outbound"]["departureCity"],
                        "departureIataCode": flight_to["outbound"]["departureIATACode"],
                        "arrivalCity": flight_to["outbound"]["arrivalCity"],
                        "arrivalIataCode": flight_to["outbound"]["arrivalIATACode"],
                        "departureDate": flight_to["outbound"]["departureDate"],
                        "arrivalDate": flight_to["outbound"]["arrivalDate"],
                        "price": flight_to["outbound"]["price"],
                        "currency": flight_to["outbound"]["currency"],
                        "priceUpdatedOn": flight_to["outbound"]["priceUpdatedOn"]},
                    "fromConnecting": {
                        "departureCity": flight_from["outbound"]["departureCity"],
                        "departureIataCode": flight_from["outbound"]["departureIATACode"],
                        "arrivalCity": flight_from["outbound"]["arrivalCity"],
                        "arrivalIataCode": flight_from["outbound"]["arrivalIATACode"],
                        "departureDate": flight_from["outbound"]["departureDate"],
                        "arrivalDate": flight_from["outbound"]["arrivalDate"],
                        "price": flight_from["outbound"]["price"],
                        "currency": flight_from["outbound"]["currency"],
                        "priceUpdatedOn": flight_from["outbound"]["priceUpdatedOn"]},
                    "summary": {
                        "timeBetweenFlights": str(
                            datetime.datetime.strptime(flight_from["outbound"]["departureDate"], "%Y-%m-%dT%H:%M:%S")
                            - datetime.datetime.strptime(flight_to["outbound"]["arrivalDate"], "%Y-%m-%dT%H:%M:%S"))
                    }
                }}
                flight_data.append(json.dumps(data))
    return flight_data