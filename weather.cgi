#!/usr/bin/python
# -*- coding: utf-8 -*-

# These are the items that can be customized for a different location.
# The zipcode is just the 5-digit code; no need for extensions.
# The station can be found by going to 
#   http://www.weather.gov/xml/current_obs/seek.php?state=il&Find=Find
# and choosing the closest NOAA station for your state.
# The radar image can be found at http://weather.com by searching
# on your location and then following the "Classic Map" link. Use
# the URL of that image here.
zipcode = '98126'
station = 'KBFI'
radar   = 'http://i.imwx.com//web/radar/us_sea_ultraradar_plus_usen.jpg'


# The code below shouldn't be modified unless you want to change the layout
# or the type of data presented.

import pywapi
import datetime
import re

# import cgitb
# cgitb.enable()

# The date and time as a string. Note: My host's server is on Eastern Time
# and I'm on Central Time, so I subtract an hour.
now = datetime.datetime.now()
now = now.strftime("%a, %b %d %I:%M %p")
# Delete leading zeros for day and hour.
now = re.sub(r' 0(\d )', r' \1', now)   # day has a space before and after
now = re.sub(r'0(\d:)', r'\1', now)     # hour has a colon after

# Get the current conditions for the given station.
noaa = pywapi.get_weather_from_noaa(station)
yahoo = pywapi.get_weather_from_yahoo(zipcode, '')

# Interpretation of the Yahoo pressure dictionary.
ypressure = {'0': 'steady', '1': 'rising', '2': 'falling'}

# Check for gusts.
try:
  gust = ', gusting to %s mph' % noaa['wind_gust_mph']
except KeyError:
  gust = ''
  
# The forecasts
today = yahoo['forecasts'][0]
tomorrow = yahoo['forecasts'][1]

# Assemble the content,.
content = '''Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta name="viewport" content = "width = device-width" />
<title>Weather - %s</title>
<style type="text/css">
  body { font-family: 'Thonburi';background-color:#002b36;color:#839496;}
  h1 { font-size: 4.5em;text-align:center;line-height:0.2em;color:#eee8d5;text-shadow:0px 2px 3px #586e75;font-family:Futura-Medium;padding-left:40px;}
  h2 {font-size: 1.1em;font-weight:400;margin-bottom:-10px;text-transform:uppercase;}
  .condition {font-size: 2em; text-align:center;line-height:0.2em;padding-top:0px;font-weight:400;}
  .small {font-size:1em;color:#657b83;}
  .forecast {}
  .forecastr {float:right;margin-top:-120px;margin-right:10px;}
  .temps{padding-left:10px;}
</style>
<link rel="apple-touch-icon-precomposed" href="http://www.b3nbrooks.com/apple-touch-icon.png" />
</head>
<body>
<h1>%.0f&deg;</h1>
<h4 class="condition">%s</h4>
<p class="small">Wind: %s at %s mph%s<br />''' % (now, float(noaa['temp_f']), yahoo['condition']['text'], noaa['wind_dir'], noaa['wind_mph'], gust )

try:
  content += 'Wind Chill: %s&deg;<br />\n' % noaa['windchill_f']
except KeyError:
  pass

content += 'Relative Humidity: %s%%<br />\n' % noaa['relative_humidity']

try:
  content += 'Heat Index: %s&deg;<br />\n' % noaa['heat_index_f']
except KeyError:
  pass

content += 'Pressure: %s and %s<br />\n' % (float(yahoo['atmosphere']['pressure']), ypressure[yahoo['atmosphere']['rising']])

content += 'Sunlight: %s to %s</p>\n' % (yahoo['astronomy']['sunrise'], yahoo['astronomy']['sunset'])



content += '''<div class="forecast"><h2>Today</h2>
<p class="temps">High: <span style="color:#cb4b16;"> %s&deg; </span><br />
Low: <span style="color:#2aa198;"> %s&deg; </span><br />
<span style="color:#268bd2;"> %s </span></p></div>
''' % (int(today['high']), int(today['low']), today['text'])

content += '''<div class="forecastr"><h2>Tomorrow</h2>
<p class="temps">High: <span style="color:#cb4b16;"> %s&deg; </span><br />
Low: <span style="color:#2aa198;"> %s&deg; </span><br />
<span style="color:#268bd2;"> %s </span></p></div>
''' % (int(tomorrow['high']), int(tomorrow['low']), tomorrow['text'])

content += '<p><img width="100%%" src="%s" /></p>\n' % radar

content += '''</body>
</html>'''

print content.encode('utf8')

