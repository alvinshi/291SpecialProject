import speech_recognition as sr
from chatterbot import ChatBot
import pyttsx

def chatbotInit():
    chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
    # Train based on the english corpus
    chatbot.train("chatterbot.corpus.english")

    # Train based on english greetings corpus
    chatbot.train("chatterbot.corpus.english.greetings")

    # Train based on the english conversations corpus
    chatbot.train("chatterbot.corpus.english.conversations")
    return chatbot

def chatbotMode(chatbot):
    engine = pyttsx.init()
    engine.say('Good morning.')
    engine.runAndWait()

    while (True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            if text == "goodbye" :
                print "Chatbot: See you next time!"
                engine.say('See you next time')
                engine.runAndWait()
                break;
            else:
                response = chatbot.get_response(text)
                engine.say(response)
                engine.runAndWait()
                print response
        except sr.UnknownValueError:
            print "Sorry, I didn't catch you."
            engine.say("sorry i didn't catch you")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return

def wheelchairMode():
    return

def standby(chatbot):
    while (True):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            #print("Google Speech Recognition thinks you said " + text)
            if text == "wake up" :
                print "I have woken up!"
                print
                chatbotMode(chatbot)
            elif (text == "I am ready wheelchair" or text == "I'm ready wheelchair"): 
                print "Here comes the wheelchair mode"
                wheelchairMode()
            elif text == "shut down":
                print
                print "The system is turning off..."
                break
        except sr.UnknownValueError:
            print
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return

def main():
    chatbot = chatbotInit()
    standby(chatbot)
    return
    
main()
