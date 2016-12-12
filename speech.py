# Third Party Libraries
import speech_recognition as sr
from chatterbot import ChatBot
import pyttsx
import threading
import eeg

#Libraries
import web
import make_call

def chatBotInit():
    chatbot = ChatBot('Roy' , trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")
    # Train based on english greetings corpus
    chatbot.train("chatterbot.corpus.english.greetings")
    # Train based on the english conversations corpus
    chatbot.train("chatterbot.corpus.english.conversations")
    return chatbot

#The speak engine does not work 
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
        #self.engine = pyttsx.init()
        
    def run(self):
        print "chat bot mode start"
        #self.engine.say("hi, what can i do for you")
        #self.engine.runAndWait()
        while (True):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print text
                if (self.data.mode == "wheelchair"):
                    if ("stop" in text):
                        self.EEG.voiceCommand = "stop"
                    elif (("exit"  in text) or ("turn off" in text)):
                        self.EEG.voiceCommand = "exit"
                        self.data.mode = "chatbot"
                else:
                    self.data.handler.informationOutputHandler(self.data, text)
                    print("You said: " + text)
                    if text == "goodbye" :
                        self.data.handler.informationOutputHandler(self.data, "See you next time!")
                        self.data.mode = "standby"
                        break;
                    elif ("ready" in text) and ("wheelchair" in text):
                        self.data.mode = "wheelchair"
                        e = eeg.EEG(self.data)
                        e.start()
                    elif ("temperature" in text) and (("now" in text) or ("outside" in text)):
                        webScrapping = web.webScrappingModule()
                        response = webScrapping.weather()
                        self.data.handler.informationOutputHandler(self.data, response)
                    elif ("weather" in text) and ("tomorrow" in text):
                        webScrapping = web.webScrappingModule()
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
    
class speechModule (threading.Thread):
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
                print text
                if (self.data.mode == "wheelchair"):
                    if ("stop" in text):
                        self.EEG.voiceCommand = "stop"
                    elif (("exit"  in text) or ("turn off" in text)):
                        self.EEG.voiceCommand = "exit"
                        self.data.mode = "standby"
                else:
                    if ("wake" in text) and ("up" in text) :
                        self.data.texts = []
                        self.data.mode = "chatbot"
                        self.chatBot.run()
                    elif ("ready" in text) and ("wheelchair" in text):
                        self.data.mode = "wheelchair"
                        e = eeg.EEG(self.data)
                        e.start()
                    elif ("help" in text) or ("call" in text):
                        self.data.mode = "call"
                        if ("help" in text):
                            self.data.callee = "+1(412)979-3573"
                            make_call.call(self.data.callee);
                    elif ("goodbye" in text):
                        self.data.mode = "standby"
                    elif text == "shut down":
                        break
            except sr.UnknownValueError:
                print("Waiting")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
