import pyowm

class webScrappingModule():
    def __init__(self):
        self.owm = pyowm.OWM('72f1ef2d8c82603b080e0c582cf3544f')
    def weather(self, location = "Pittsburgh, US", inDetailed = True):
        observation = self.owm.weather_at_place(location)
        w = observation.get_weather()
        if (not inDetailed):
            return "%1.1f, degress celsius" %(w.get_temperature('celsius')['temp'])
        else:
            result = "It's %1.1f degress celsius out there\n" %(w.get_temperature('celsius')['temp'])
            return result

    def weatherForcast(self, location = "Pittsburgh, US"):
        return
        #forecast = self.owm.daily_forecast(location)
        #tomorrow = pyowm.timeutils.tomorrow()
        #print tomorrow
        #return tomorrow
