# Third Party Libraries
from tkinter import *
import threading
import time
from time import gmtime, strftime
from datetime import datetime
from pytz import timezone
import math
#import eeg

# Libaries
import speech

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
def init(data):
    # load data.xyz as appropriate
    data.texts = []
    data.mode = "standby"
    data.chatBot = speech.chatBotInit() # Blocking I/O
    class Struct(object): pass
    data.EEG = Struct()
    data.EEG.curCommand = "neutral"
    data.EEG.voiceCommand = ""
    data.EEG.speed = 0
    data.EEG.battery = "NONE"
    data.EEG.contact = "NONE"
    data.EEG.signal = "NONE"
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
                       text = "Signal Strength : " + str(data.EEG.signal),
                       font = ("Helevetica", "10"),
                       fill = "WHITE")
    canvas.create_text(data.width // 2 + 150, data.height * 0.03,
                       text = "Battery : " + str(data.EEG.battery),
                       font = ("Helevetica", "10"),
                       fill = "WHITE")

    #Wheelchair Control
    motion = data.EEG.curCommand
    canvas.create_rectangle(data.width // 2 - 30, data.height // 2 - 30,
                            data.width // 2 + 30, data.height // 2 + 30,
                            fill = "White",
                            width = 3)
    #Accelerate
    canvas.create_polygon(data.width // 2 - 30, data.height // 2 - 50,
                          data.width // 2 + 30, data.height // 2 - 50,
                          data.width // 2, data.height // 2 - 50 - 30 * math.sqrt(2),
                          fill = ("Yellow" if motion == "forward" else "White"),
                          width = 3,
                          outline = "Black")

    #Decelerate
    canvas.create_polygon(data.width // 2 - 30, data.height // 2 + 45,
                          data.width // 2 + 30, data.height // 2 + 45,
                          data.width // 2, data.height // 2 + 45 + 30 * math.sqrt(2),
                          fill = ("Yellow" if motion == "backward" else "White"),
                          width = 3,
                          outline = "Black")
    
    #Left
    canvas.create_polygon(data.width // 2 - 45, data.height // 2 - 30,
                          data.width // 2 - 45, data.height // 2 + 30,
                          data.width // 2 - 45 - 30 * math.sqrt(2), data.height // 2, 
                          fill = ("Yellow" if motion == "left" else "White"),
                          width = 3,
                          outline = "Black")

    #Right
    canvas.create_polygon(data.width // 2 + 45, data.height // 2 - 30,
                          data.width // 2 + 45, data.height // 2 + 30,
                          data.width // 2 + 45 + 30 * math.sqrt(2), data.height // 2, 
                          fill = ("Yellow" if motion == "right" else "White"),
                          width = 3,
                          outline = "Black")

    #Speed
    canvas.create_text(data.width // 2, data.height * 0.75,
                       text = str(data.EEG.speed) + " cm/s",
                       font = ("Helevetica", "25"),
                       fill = "WHITE")
    
    #Warnings
    canvas.create_text(data.width // 2, data.height * 0.80,
                       text = "take care and enjoy the ride",
                       font = ("Helevetica", "15"),
                       fill = "WHITE")

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
    sr = speech.speechModule("Speech Module", data)
    sr.start()
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print "bye!" 
run()
