import datetime
import click
import json
from prettytable import PrettyTable
from FlightFinderApp_JG.FlightManager import RyanairFlights
from FlightFinderApp_JG.DestinationManager import RyanairDestinations

@click.group()
def cli():
    pass

@click.command()
@click.option("-d", "--departurecode", required=True, help="The starting point of your trip. Specify your departure airport code")
@click.option("-a", "--arrivalcode", help="The final point of your trip. Specify your arrival airport code")
@click.option("-r", "--includereturnflight", is_flag=True, help="Includes return flights into search results")
@click.option("-o", "--outbounddatefrom", help="Start date of your trip. If not specified, then today date is set")
@click.option("-p", "--pricevalue", type=int, default=999, show_default=True, help="Max price for one way / return flights. It does not apply to total price of connecting flights")
@click.option("-f", "--dateflexibility", type=int, default=2, show_default=True, help="Extends the search period by so many days (outbound date +/- date flexibility)")
@click.option("-t", "--tripduration", type=int, default=7, show_default=True, help="Date of the return flight is set by adding the trip duration to outbound date")
def findFlights(departurecode, arrivalcode, includereturnflight, outbounddatefrom, pricevalue, dateflexibility, tripduration):

    table = PrettyTable()
    ryanairFlights = RyanairFlights()

    """Find flights from your departure airport to all available destinations (if arrival airport is not specified) 
    or to the selected one.

    Departure Code is a code of airport that is selected for departure.
    """
    if not outbounddatefrom:
        outbounddatefrom = str(datetime.date.today())

    result = ryanairFlights.find_flights(departure_airport_code=departurecode,
                                         arrival_airport_code=arrivalcode,
                                         is_return_trip=includereturnflight,
                                         price_value_to=pricevalue,
                                         outbound_date=outbounddatefrom,
                                         date_flexibility_in_days=dateflexibility,
                                         trip_duration_in_days=tripduration)

    if result is not None:
        if not includereturnflight:
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

@click.command()
@click.option("--city", type=str, help="Returns a list of airport codes that are bases of Ryanair in the specified city")
@click.option("--country", type=str, help="Returns a list of cities and airport codes that are bases of Ryanair in the specified country")
def findAirportCode(city, country):
    ryanairDestination = RyanairDestinations()
    table = PrettyTable()

    """Find airport IATA codes by city or country. Airport code is used to search for flights. 
    """


    if city and country is None:
        try:
            result = ryanairDestination.get_active_airport_codes_by_city(city=city)
            table.field_names = ["City Airport", "Airport code"]
            for item in result:
                table.add_row([item, result[item]])
        except Exception as e:
            print(e)
            print("Something went wrong with specified city: %s" %(city))
    elif country and city is None:
        try:
            result = ryanairDestination.get_active_airports_by_country(country=country)
            if result:
                table.field_names = ["City", "City Airport", "Airport code"]
                for item in result:
                    for inner in result[item]:
                        for key in inner:
                            table.add_row([item, key, inner[key]], divider=True)
            else:
                print("No Ryanair airports found in specified country. Specified country: %s" %(country))
        except Exception as e:
            print(e)
            print("Tried to search by country but something went wrong with it. Specified country: %s" %(country))
    elif city and country:
        try:
            result = ryanairDestination.get_active_airports_by_country(country=country)
            if result:
                table.field_names = ["City", "City Airport", "Airport code"]
                for item in result:
                    for inner in result[item]:
                        for key in inner:
                            table.add_row([item, key, inner[key]], divider=True)
            else:
                print("No Ryanair airports found in specified country. Specified country: %s" %(country))
        except Exception as e:
            print(e)
            print("Tried to search by country but something went wrong with it. Specified country: %s" %(country))
    else:
        print("Try to specify at least one option and maybe it will helps")

    print(table)


cli.add_command(findFlights)
cli.add_command(findAirportCode)
def main():
    cli()