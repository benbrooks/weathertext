`Weathertext` is a short Python script that prints current weather information and forecasts gathered from NOAA, Yahoo!, and/or Google via the [`pywapi` library][1]. It's primary intent is to be called by [GeekTool][2] or [Growl][5] to display the information on a Mac.

A longer description of the goals of `weathertext` and its use of `pywapi` can be found in [this blog post][3] and [this one][4]. Here's a way to configure GeekTool to run `weathertext` every 15 minutes:

<img class="ss" src="http://www.leancrew.com/all-this/images/gt-weathertext-iconv.png" />

And here's a shell pipeline that puts the info in a Growl window:

		~/bin/weathertext | /usr/local/bin/growlnotify -t Weather

[1]: http://code.google.com/p/python-weather-api/
[2]: http://projects.tynsoe.org/en/geektool/
[3]: http://www.leancrew.com/all-this/2009/06/new-weather-script-for-geektool/
[4]: http://www.leancrew.com/all-this/2009/12/geektool-desktop-weather-with-forecasts/
[5]: http://growl.info/
