from datetime import date
from datetime import timedelta
import urllib2
import json

startdate = date.today()
BASE_RATE_URL = "https://www.thebookingbutton.com.au/api/v2/reloaded/properties/57hoteldirect/room_rates?check_in_date=%s&check_out_date=%s&locale=en&promotion_code=10off"
BASE_ROOM_URL = "https://www.thebookingbutton.com.au/api/v2/reloaded/properties/57hoteldirect/room_types?check_in_date=%s&check_out_date=%s"

def LowestRateForRoomOnNight(room_id, start_date):
  end_date = start_date + timedelta(1)
  return LowestRateForRoomForStay(room_id, start_date, end_date)

def LowestRateForRoomForStay(room_id, start_date, end_date):
  lowest_rate = 999999

  url = BASE_ROOM_URL % (start_date, end_date)
  response = urllib2.urlopen(url)
  html = response.read()
  room_response = json.loads(html)
  available = True
  for room in room_response:
    if room['id'] in (room_id,):
      #print json.dumps(room, indent=3)
      for roomdate in room["room_type_dates"]:
        available &= roomdate["available"] > 0
        # print str(roomdate) + " - " + str(roomdate["available"] > 0)
  #print available
  
  if available:
    url = BASE_RATE_URL % (start_date, end_date)
    # print url
    response = urllib2.urlopen(url)
    html = response.read()
    rate_response = json.loads(html)
    for room in rate_response:
      if room['room_type_id'] in (room_id,):
        #print json.dumps(room, indent=3)
        valid_prices = True
        total_price = 0
        for rateinfo in room['room_rate_dates']:
          # print json.dumps(rateinfo, indent=3)
          if rateinfo["stop_sell"]:
              valid_prices = False
          else:
              total_price += rateinfo['rate']
              
        if valid_prices and (total_price < lowest_rate):
            lowest_rate = total_price

  if lowest_rate == 999999:  
    return None
  else:
    return lowest_rate


# Single Night Test
#for i in range(2,6):
#  startdate = date.today() + timedelta(i)
#  print str(startdate) + ": " + str(LowestRateForRoomOnNight(103576, startdate))
  
# Multi Night Test
for i in range(2,6):
  startdate = date.today() + timedelta(i)
  enddate = date.today() + timedelta(i+3)
  print str(startdate) + "-" + str(enddate) + ": " + str(LowestRateForRoomForStay(103576, startdate, enddate))
