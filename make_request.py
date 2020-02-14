import requests
import pprint

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))




query  = """
{
  plan(
    fromPlace: "Hakaniemi, Helsinki::60.179267,24.951501",
    toPlace: "Keilaniemi, Espoo::60.1762,24.836584",
    date: "2020-02-12",
    time: "20:28:00",
    numItineraries: 5,
    transportModes: [{mode: BUS}, {mode: RAIL}, {mode:TRAM}, {mode: FERRY}, {mode:WALK}]
    walkReluctance: 2.1,
    walkBoardCost: 300,
    minTransferTime: 600,
    walkSpeed: 1.7,
  ) {
    itineraries{
      walkDistance
      duration
      legs {
        mode
        startTime
        endTime
        from {
          name
          stop {
            code
            name
          }
        }
        to {
          name
          stop {
            code
            name
          }
        }
        trip {
        	tripHeadsign
          routeShortName
        }
        distance
        
      }
    }
  }
}

"""

result=run_query(query)
print(type(result))
