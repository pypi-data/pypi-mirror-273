import datetime
import json
from prettytable import PrettyTable
from FlightFinderApp_JG.FlightManager import RyanairFlights

table = PrettyTable()
ryanairFlights = RyanairFlights()


_departure_airport = "KUN"
_arrival_airport = "OPO"
_includeReturnFlight = True
_dateFrom = str(datetime.date.today())
_price_value = 50

result = ryanairFlights.find_flights(departure_airport_code=_departure_airport,
                                     arrival_airport_code=_arrival_airport,
                                     is_return_trip=_includeReturnFlight,
                                     outbound_date=_dateFrom,
                                     date_flexibility_in_days=10,
                                     trip_duration_in_days=10)

if result is not None:
    if not _includeReturnFlight:
        table.field_names = ["Total Trip Price", "Flight From", "Flight To", "Departure date", "Arrival date"]

        for item in result:
            data = json.loads(item)
            if "toConnecting" in data["outbound"]:
                table.add_row([
                    str(data["outbound"]["toConnecting"]["price"])+" ("+data["outbound"]["toConnecting"]["currency"]+")",
                    data["outbound"]["toConnecting"]["departureCity"]+" ("+data["outbound"]["toConnecting"]["departureIataCode"]+")",
                    data["outbound"]["toConnecting"]["arrivalCity"]+" ("+data["outbound"]["toConnecting"]["arrivalIataCode"]+")",
                    data["outbound"]["toConnecting"]["departureDate"],
                    data["outbound"]["toConnecting"]["arrivalDate"]])
                table.add_row([
                    str(data["outbound"]["fromConnecting"]["price"])+" ("+data["outbound"]["fromConnecting"]["currency"]+")",
                    data["outbound"]["fromConnecting"]["departureCity"]+" ("+data["outbound"]["fromConnecting"]["departureIataCode"]+")",
                    data["outbound"]["fromConnecting"]["arrivalCity"]+" ("+data["outbound"]["fromConnecting"]["arrivalIataCode"]+")",
                    data["outbound"]["fromConnecting"]["departureDate"],
                    data["outbound"]["fromConnecting"]["arrivalDate"]], divider=True)
            else:
                table.add_row([
                    str(data["outbound"]["price"])+" ("+data["outbound"]["currency"]+")",
                    data["outbound"]["departureCity"]+" ("+data["outbound"]["departureIATACode"]+")",
                    data["outbound"]["arrivalCity"]+" ("+data["outbound"]["arrivalIATACode"]+")",
                    data["outbound"]["departureDate"],
                    data["outbound"]["arrivalDate"]])

    else:
        table.field_names = ["Total Trip Price", "Trip Duration", "Outbound Flight", "Outbound Departure Date", "Outbound Arrival Date", "Outbound Flight Price", "Inbound Flight", "Inbound Departure Date", "Inbound Arrival Date", "Inbound Flight Price"]

        for item in result:
            data = json.loads(item)

            if "toConnecting" in data["outbound"]:
                table.add_row([
                    str(data["tripSummary"]["totalPrice"]),
                    data["tripSummary"]["tripDuration"] + " (" + data["tripSummary"]["timeInDestination"] + ")",
                    data["outbound"]["toConnecting"]["departureCity"]+" ("+data["outbound"]["toConnecting"]["departureIataCode"]+")"
                        + " - " + data["outbound"]["toConnecting"]["arrivalCity"]
                        + " (" + data["outbound"]["toConnecting"]["arrivalIataCode"]+")",
                    data["outbound"]["toConnecting"]["departureDate"],
                    data["outbound"]["toConnecting"]["arrivalDate"],
                    str(data["outbound"]["toConnecting"]["price"]) + " ("+data["outbound"]["toConnecting"]["currency"]+")",
                    data["inbound"]["toConnecting"]["departureCity"] + " ("+data["inbound"]["toConnecting"]["departureIataCode"]+")"
                        + " - " + data["inbound"]["toConnecting"]["arrivalCity"]
                    + "("+data["inbound"]["toConnecting"]["arrivalIataCode"],
                    data["inbound"]["toConnecting"]["departureDate"],
                    data["inbound"]["toConnecting"]["arrivalDate"],
                    str(data["inbound"]["toConnecting"]["price"])+" ("+data["inbound"]["toConnecting"]["currency"]+")"])
                table.add_row([
                    "-",
                    "-",
                    data["outbound"]["fromConnecting"]["departureCity"]+" ("+data["outbound"]["fromConnecting"]["departureIataCode"]+")"
                        + " - " +data["outbound"]["fromConnecting"]["arrivalCity"]
                        + "("+data["outbound"]["fromConnecting"]["arrivalIataCode"]+")",
                    data["outbound"]["fromConnecting"]["departureDate"],
                    data["outbound"]["fromConnecting"]["arrivalDate"],
                    str(data["outbound"]["fromConnecting"]["price"])+" ("+data["outbound"]["fromConnecting"]["currency"]+")",
                    data["inbound"]["fromConnecting"]["departureCity"]+" ("+data["inbound"]["fromConnecting"]["departureIataCode"]+")"
                        + " - " +data["inbound"]["fromConnecting"]["arrivalCity"]
                        + "("+data["inbound"]["fromConnecting"]["arrivalIataCode"]+")",
                    data["inbound"]["fromConnecting"]["departureDate"],
                    data["inbound"]["fromConnecting"]["arrivalDate"],
                    str(data["inbound"]["fromConnecting"]["price"])+" ("+data["inbound"]["fromConnecting"]["currency"]+")"], divider=True)
            else:
                table.add_row([
                    str(data["summary"]["price"]),
                    data["summary"]["tripDuration"],
                    data["outbound"]["departureCity"]+" ("+data["outbound"]["departureIATACode"]+")",
                    data["outbound"]["departureDate"],
                    data["outbound"]["arrivalDate"],
                    str(data["outbound"]["price"])+" ("+data["outbound"]["currency"]+")",
                    data["inbound"]["departureCity"]+" ("+data["inbound"]["departureIATACode"]+")",
                    data["inbound"]["departureDate"],
                    data["inbound"]["arrivalDate"],
                    str(data["inbound"]["price"])+" ("+data["inbound"]["currency"]+")"])

    print(table)
