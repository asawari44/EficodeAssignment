from flask import Flask
from flask import render_template, request
import requests
from geopy import Nominatim
import os
from make_request import run_query
import json
import time
import datetime

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def get_destination():
   ## return "Hello {}!".format("c")

#https://maps.googleapis.com/maps/api/js?key=AIzaSyDkhgQK2cM1nHlv6TcgffFjVO_aZIaHUW0&callback=initMap
  if request.method == 'POST':
    location_detail = request.form["location"]
    location_detail = location_detail.strip()
    if(location_detail != ''):
      key = "AIzaSyDkhgQK2cM1nHlv6TcgffFjVO_aZIaHUW0"
      os.environ["GOOGLE_API_KEY"] =key
      locator = Nominatim(user_agent="myGeocoder")
      location = locator.geocode(location_detail)
      #print(location)
      latitude = location.latitude
      longitude = location.longitude
      print(latitude,longitude)
      date= datetime.datetime.now().date().isoformat()
      time= datetime.datetime.now().time().isoformat()
      fromPlace= "Pohjoinen Rautatiekatu 25, Helsinki::60.169392,24.925751"
      toPlace= str(location_detail.strip())+"::"+str(latitude)+","+str(longitude)

      subquery = "fromPlace: \""+fromPlace+"\",toPlace: \""+toPlace+"\",date: \""+date+"\",time:\""+time+"\"," 
      query  = """
{
  plan("""+subquery+"""
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
      #print(result["data"]["plan"]["itineraries"])
      #results=eval(json.dumps(result))

      for item in result["data"]["plan"]["itineraries"]:
          for leg in item["legs"]:
              distance = leg["distance"]
              leg["distance"] = float(distance/1000)
              startTime=datetime.datetime.fromtimestamp(int(leg["startTime"]/1000))
         
              endTime= datetime.datetime.fromtimestamp(int(leg["endTime"]/1000)) 
              leg["startTime"]=startTime.time().isoformat()
        
              leg["endTime"]=endTime.time().isoformat()         
              
      return render_template('result.html',items=result["data"]["plan"]["itineraries"])
      
    else:
      latitude = "No input given"
      longitude = "No input given"
      formatted_address = "No input given"
      print("no input!!!")
    #return render_template("result.html",result = formatted_address,Latitude=latitude,longitude=longitude)
  return render_template('get_destination.html', title='Find Your Way Home!')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True )

#{b: 24.827682, a: 60.1866693}
