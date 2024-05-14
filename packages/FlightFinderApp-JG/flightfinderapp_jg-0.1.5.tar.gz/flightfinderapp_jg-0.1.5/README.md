Flight Finder App is a Python package for searching flights (only Ryanair at the moment). It provides Command-line interface (CLI) capabilities for aquick and simple search
or could be used as a library in your code. 

Installation
============
````
pip install FlightFinderApp-JG
````

Using command-line interface
---------------
Flight Finder App CLI provides two commands:
* _findFlights_
* _findAirportCode_

````
Usage: FlightFinderApp findflights [OPTIONS]

Options:
  -d, --departurecode TEXT       The starting point of your trip. Specify your
                                 departure airport code
  -a, --arrivalcode TEXT         The final point of your trip. Specify your
                                 arrival airport code
  -r, --includereturnflight      Includes return flights into search results
  -o, --outbounddatefrom TEXT    Start date of your trip. If not specified,
                                 then today date is set
  -p, --pricevalue INTEGER       Max price for one way / return flights. It
                                 does not apply to total price of connecting
                                 flights  [default: 999]
  -f, --dateflexibility INTEGER  Extends the search period by so many days
                                 (outbound date +/- date flexibility)
                                 [default: 2]
  -t, --tripduration INTEGER     Date of the return flight is set by adding
                                 the trip duration to outbound date  [default:
                                 7]

Usage: FlightFinderApp findairportcode [OPTIONS]

Options:
  --city TEXT     Returns a list of airport codes that are bases of Ryanair in
                  the specified city
  --country TEXT  Returns a list of cities and airport codes that are bases of
                  Ryanair in the specified country
````
Using as a library
-----

Creating an instance:
```python
from FlightFinderApp_JG.FlightManager import RyanairFlights

ryanairFlights = RyanairFlights()
```

All you need is the ***find_flights*** function. To search for a return flight between two airports which 
price is bellow 50Eur

```python
ryanairFlights.find_flights(departure_airport_code="KUN",
                            arrival_airport_code="BER",
                            is_return_trip=True,
                            price_value_to=50)
```
Result:
```json
{
  "outbound": {
    "departureCountry": "Lithuania",
    "departureCity": "Kaunas",
    "departureIATACode": "KUN",
    "arrivalCountry": "Germany",
    "arrivalCity": "Berlin",
    "arrivalIATACode": "BER",
    "departureDate": "2024-05-14T09:50:00",
    "arrivalDate": "2024-05-14T10:30:00",
    "price": 21.99,
    "currency": "EUR",
    "priceUpdatedOn": 1715243865000
  },
  "summary": {
    "price": 34.98,
    "currency": "EUR",
    "tripDuration": 7
  },
  "inbound": {
    "departureCountry": "Germany",
    "departureCity": "Berlin",
    "departureIATACode": "BER",
    "arrivalCountry": "Lithuania",
    "arrivalCity": "Kaunas",
    "arrivalIATACode": "KUN",
    "departureDate": "2024-05-21T06:35:00",
    "arrivalDate": "2024-05-21T09:10:00",
    "price": 12.99,
    "currency": "EUR",
    "priceUpdatedOn": 1715237050000
  }
}
```
If no results are returned, try to specify the following parameters:
* _date_flexibility_in_days_
* _trip_duration_in_days_

```python
ryanairFlights.find_flights(departure_airport_code="KUN",
                            arrival_airport_code="BER",
                            is_return_trip=True,
                            price_value_to=50,
                            date_flexibility_in_days=5,
                            trip_duration_in_days=10)
```
If direct flight between two airports is not found, then a connecting flight could be suggested (if such exists, 
remember, we're operating only with ***Ryanair*** flights)

Searching for a flight between two airports, but we already know that direct flight does not exist. 
Also, we have defined our trip start date: 

```python
ryanairFlights.find_flights(departure_airport_code="KUN",
                            arrival_airport_code="OPO",
                            is_return_trip=True,
                            outbound_date="2024-06-10",
                            date_flexibility_in_days=10,
                            trip_duration_in_days=10)
```
Result:
```json
{
  "outbound": {
    "toConnecting": {
      "departureCity": "Kaunas",
      "departureIataCode": "KUN",
      "arrivalCity": "Alicante",
      "arrivalIataCode": "ALC",
      "departureDate": "2024-06-04T06:00:00",
      "arrivalDate": "2024-06-04T09:00:00",
      "price": 97.81,
      "currency": "EUR",
      "priceUpdatedOn": 1715247806000
    },
    "fromConnecting": {
      "departureCity": "Alicante",
      "departureIataCode": "ALC",
      "arrivalCity": "Porto",
      "arrivalIataCode": "OPO",
      "departureDate": "2024-06-05T11:40:00",
      "arrivalDate": "2024-06-05T12:20:00",
      "price": 19.99,
      "currency": "EUR",
      "priceUpdatedOn": 1715236900000
    },
    "summary": {
      "timeBetweenFlights": "1 day, 2:40:00"
    }
  },
  "inbound": {
    "toConnecting": {
      "departureCity": "Porto",
      "departureIataCode": "OPO",
      "arrivalCity": "Alicante",
      "arrivalIataCode": "ALC",
      "departureDate": "2024-06-20T10:55:00",
      "arrivalDate": "2024-06-20T13:30:00",
      "price": 19.99,
      "currency": "EUR",
      "priceUpdatedOn": 1715236759000
    },
    "fromConnecting": {
      "departureCity": "Alicante",
      "departureIataCode": "ALC",
      "arrivalCity": "Kaunas",
      "arrivalIataCode": "KUN",
      "departureDate": "2024-06-22T07:10:00",
      "arrivalDate": "2024-06-22T12:00:00",
      "price": 162.99,
      "currency": "EUR",
      "priceUpdatedOn": 1715247391000
    },
    "summary": {
      "timeBetweenFlights": "1 day, 17:40:00"
    }
  },
  "tripSummary": {
    "totalPrice": "300.78",
    "tripDuration": "18 days, 6:00:00",
    "timeInDestination": "14 days, 22:35:00"
  }
}
```