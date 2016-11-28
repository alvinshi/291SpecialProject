from tkinter import *
import speech_recognition as sr
from chatterbot import ChatBot
import pyttsx
import threading
import time
from time import gmtime, strftime
from datetime import datetime
from pytz import timezone
import math
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
        
    
class speakEngine(threading.Thread):
    def __init__(self, response):
        threading.Thread.__init__(self)
        self.engine = pyttsx.init()
        self.response = response
        
    def run(self):
        self.engine.say(self.response)
        self.engine.runAndWait()
        
class chatBot():
    def __init__(self, data):
        self.data = data
        self.engine = pyttsx.init()
        
    def run(self):
        print "chat bot mode start"
        while (True):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                self.data.handler.informationOutputHandler(self.data, text)
                print("You said: " + text)
                if text == "goodbye" :
                    self.data.handler.informationOutputHandler(self.data, "See you next time!")
                    self.data.mode = "standby"
                    break;
                elif ("ready" in text) and ("wheelchair" in text):
                    self.data.mode = "wheelchair"
                    #wheelchairMode()
                    print
                elif ("temperature" in text) and (("now" in text) or ("outside" in text)):
                    webScrapping = webScrappingModule()
                    response = webScrapping.weather()
                    self.data.handler.informationOutputHandler(self.data, response)
                elif ("weather" in text) and ("tomorrow" in text):
                    webScrapping = webScrappingModule()
                    response = webScrapping.weatherForcast()
                    self.data.handler.informationOutputHandler(self.data, response)
                else:
                    response = self.data.chatBot.get_response(text)
                    print response
                    self.data.handler.informationOutputHandler(self.data, response)
            except sr.UnknownValueError:
                print "Unknown Value Error"
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
class speechModule (threading.Thread) :
    def __init__(self, name, data):
        threading.Thread.__init__(self)
        self.name = name
        self.data = data
        self.chatBot = chatBot(data)

    def run(self):
        while (True):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                if ("wake" in text) and ("up" in text) :
                    self.data.texts = []
                    self.data.mode = "chatbot"
                    self.chatBot.run()
                elif ("ready" in text) and ("wheelchair" in text):
                    self.data.mode = "wheelchair"
                    #wheelchairMode()
                    print
                elif ("help" in text) or ("call" in text):
                    self.data.mode = "call"
                    if ("help" in text):
                        self.data.callee = "911"
                    else:
                        self.data.callee = "+1(412)320-0542"
                    #wheelchairMode()
                    print
                elif text == "shut down":
                    break
            except sr.UnknownValueError:
                print("Waiting")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
####################################
# handlers
####################################
class eventHandler():
    def informationOutputHandler(self, data, text):
        data.texts.append(text)

    def modeHandler(self, data, newMode):
        data.texts.mode = newMode
        
####################################
# customize these functions
####################################
def chatBotInit():
    chatbot = ChatBot('Alvin' , trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")
    # Train based on english greetings corpus
    chatbot.train("chatterbot.corpus.english.greetings")
    # Train based on the english conversations corpus
    chatbot.train("chatterbot.corpus.english.conversations")
    return chatbot

def init(data):
    # load data.xyz as appropriate
    data.texts = []
    data.mode = "standby"
    data.chatBot = chatBotInit() # Blocking I/O
    pass

def initImg(data):
    data.img = {}
    data.img["welcomeBg"] = PhotoImage(file = "img/welcomeBg.gif")
    data.img["phone"] = PhotoImage(file = "img/phone.gif")

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    pass

def redrawAllStandby(canvas, data):
    #Background
    canvas.create_image(0, 0, image = data.img["welcomeBg"], anchor = NW)

    #Time Information
    now_date= datetime.now(timezone('US/Eastern'))
    now_time= datetime.now(timezone('US/Eastern'))
    date = now_date.strftime("%Y / %m / %d")
    time = now_time.strftime("%H:%M")
    canvas.create_text(data.width // 2, data.height * 0.2,
                       text = time,
                       font = ("Helevetica", "70"),
                       fill = "WHITE")
    canvas.create_text(data.width // 2, data.height * 0.30,
                       text = date,
                       font = ("Helevetica", "20"),
                       fill = "WHITE")

    #Company Stamp
    canvas.create_text(data.width // 2, data.height * 0.8,
                       text = "Brought to you by",
                       font = ("Helevetica", "13"),
                       fill = "White")
    canvas.create_text(data.width // 2, data.height * 0.84,
                       text = " R & A Inc.",
                       font = ("Comic Sans MS", "20"),
                       fill = "White")

def redrawAllChatbot(canvas, data):
    #Background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="RoyalBlue2", width = 0)
    #Header
    #Time Information
    now_time= datetime.now(timezone('US/Eastern'))
    time = now_time.strftime("%H:%M")
    canvas.create_text(data.width // 2 - 170, data.height * 0.03,
                       text = time,
                       font = ("Helevetica", "10"),
                       fill = "WHITE")
    canvas.create_text(data.width // 2 + 150, data.height * 0.03,
                       text = "Internet : Good",
                       font = ("Helevetica", "10"),
                       fill = "WHITE")

    if (len(data.texts) == 0):
        canvas.create_text(data.width // 2, data.height * 0.3,
                       text = "What can I do for you?",
                       font = ("Helevetica", "25"),
                       fill = "White")
        canvas.create_line(data.width // 2 - 120, data.height * 0.35,
                           data.width // 2 + 120, data.height * 0.35,
                           fill = "WHITE")

    else:
        for i in range(max(0, len(data.texts) - 12),len(data.texts)):
            index = i - max(0, len(data.texts) - 12);
            if (i % 2 == 0):
                canvas.create_text(20, 40 * (2 + index), anchor = W,
                                   text = data.texts[i],
                                   font = ("Helevetica", "15"),
                                   fill = "WHITE")
            else:
                assert(i % 2 == 1)
                canvas.create_text(data.width - 20, 40 * (2 + index), anchor = E,
                                   text = data.texts[i],
                                   font = ("Helevetica", "15"),
                                   fill = "WHITE")

def redrawAllWheelchair(canvas, data):
    #Background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="RoyalBlue2", width = 0)
    #Header
    now_time= datetime.now(timezone('US/Eastern'))
    time = now_time.strftime("%H:%M")
    canvas.create_text(data.width // 2 - 170, data.height * 0.03,
                       text = time,
                       font = ("Helevetica", "10"),
                       fill = "WHITE")
    canvas.create_text(data.width // 2, data.height * 0.03,
                       text = "Signal Strength: Weak",
                       font = ("Helevetica", "10"),
                       fill = "WHITE")
    canvas.create_text(data.width // 2 + 150, data.height * 0.03,
                       text = "Internet : Good",
                       font = ("Helevetica", "10"),
                       fill = "WHITE")

    #Wheelchair Control
    canvas.create_rectangle(data.width // 2 - 30, data.height // 2 - 30,
                            data.width // 2 + 30, data.height // 2 + 30,
                            fill = "White",
                            width = 3)
    #Accelerate
    canvas.create_polygon(data.width // 2 - 30, data.height // 2 - 50,
                          data.width // 2 + 30, data.height // 2 - 50,
                          data.width // 2, data.height // 2 - 50 - 30 * math.sqrt(2),
                          fill = "White",
                          width = 3,
                          outline = "Black")

    #Decelerate
    canvas.create_polygon(data.width // 2 - 30, data.height // 2 + 45,
                          data.width // 2 + 30, data.height // 2 + 45,
                          data.width // 2, data.height // 2 + 45 + 30 * math.sqrt(2),
                          fill = "White",
                          width = 3,
                          outline = "Black")
    
    #Left
    canvas.create_polygon(data.width // 2 - 45, data.height // 2 - 30,
                          data.width // 2 - 45, data.height // 2 + 30,
                          data.width // 2 - 45 - 30 * math.sqrt(2), data.height // 2, 
                          fill = "White",
                          width = 3,
                          outline = "Black")

    #Right
    canvas.create_polygon(data.width // 2 + 45, data.height // 2 - 30,
                          data.width // 2 + 45, data.height // 2 + 30,
                          data.width // 2 + 45 + 30 * math.sqrt(2), data.height // 2, 
                          fill = "White",
                          width = 3,
                          outline = "Black")

def redrawAllCall(canvas, data):
    #Background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="RoyalBlue2", width = 0)
    #Header
    now_time= datetime.now(timezone('US/Eastern'))
    time = now_time.strftime("%H:%M")
    canvas.create_text(data.width // 2 - 170, data.height * 0.03,
                       text = time,
                       font = ("Helevetica", "10"),
                       fill = "WHITE")
    canvas.create_text(data.width // 2 + 150, data.height * 0.03,
                       text = "Internet : Good",
                       font = ("Helevetica", "10"),
                       fill = "WHITE")
    #Phone Panel
    canvas.create_image(data.width // 2, data.height // 2 - 20,
                        image = data.img["phone"],
                        anchor = CENTER)
    canvas.create_text(data.width // 2, data.height // 2 + 120,
                       text = "Calling " + data.callee + " ...",
                       font = ("Helevetica", "30"),
                       fill = "WHITE")
    
    

def redrawAll(canvas, data):
    # draw in canvas
    if (data.mode == "standby") :
        redrawAllStandby(canvas, data)
    elif (data.mode == "chatbot") :
        redrawAllChatbot(canvas, data)
    elif (data.mode == "wheelchair") :
        redrawAllWheelchair(canvas, data)
    elif (data.mode == "call") :
        redrawAllCall(canvas, data)
    else:
        print "Unknown mode"
        exit(-1)
        
####################################
# use the run function as-is
####################################

def run(width=400, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    initImg(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # event handler
    handler = eventHandler()
    data.handler = handler
    # launch the speech_recognition thread
    sr = speechModule("Speech Module", data)
    sr.start()
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print "bye!" 
run()
