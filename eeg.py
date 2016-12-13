import sys
import os
import platform
import time
import ctypes
import create
import threading

# Imports the library
if sys.platform.startswith('win32'):
    import msvcrt
else:
    print 'Not windows system.';

from ctypes import *

try:
    if sys.platform.startswith('win32'):
        libEDK = cdll.LoadLibrary("bin/win64/edk.dll")
    else:
        raise Exception('System not supported.')
except Exception as e:
    print 'Error: cannot load EDK lib:', e
    exit()

write = sys.stdout.write

IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
IEE_EmoEngineEventCreate.argtypes = []
IEE_EmoEngineEventCreate.restype = c_void_p

IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
IEE_EmoStateCreate.restype = c_void_p
eState = IEE_EmoStateCreate()

IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
IEE_EmoEngineEventGetEmoState.restype = c_int

IS_GetTimeFromStart = libEDK.IS_GetTimeFromStart
IS_GetTimeFromStart.argtypes = [ctypes.c_void_p]
IS_GetTimeFromStart.restype = c_float

IS_GetWirelessSignalStatus = libEDK.IS_GetWirelessSignalStatus
IS_GetWirelessSignalStatus.restype = c_int
IS_GetWirelessSignalStatus.argtypes = [c_void_p]

IS_FacialExpressionIsBlink = libEDK.IS_FacialExpressionIsBlink
IS_FacialExpressionIsBlink.restype = c_int
IS_FacialExpressionIsBlink.argtypes = [c_void_p]

IS_FacialExpressionIsLeftWink = libEDK.IS_FacialExpressionIsLeftWink
IS_FacialExpressionIsLeftWink.restype = c_int
IS_FacialExpressionIsLeftWink.argtypes = [c_void_p]

IS_FacialExpressionIsRightWink = libEDK.IS_FacialExpressionIsRightWink
IS_FacialExpressionIsRightWink.restype = c_int
IS_FacialExpressionIsRightWink.argtypes = [c_void_p]

IS_FacialExpressionGetUpperFaceAction =  \
    libEDK.IS_FacialExpressionGetUpperFaceAction
IS_FacialExpressionGetUpperFaceAction.restype = c_int
IS_FacialExpressionGetUpperFaceAction.argtypes = [c_void_p]

IS_FacialExpressionGetUpperFaceActionPower = \
    libEDK.IS_FacialExpressionGetUpperFaceActionPower
IS_FacialExpressionGetUpperFaceActionPower.restype = c_float
IS_FacialExpressionGetUpperFaceActionPower.argtypes = [c_void_p]

IS_FacialExpressionGetLowerFaceAction = \
    libEDK.IS_FacialExpressionGetLowerFaceAction
IS_FacialExpressionGetLowerFaceAction.restype = c_int
IS_FacialExpressionGetLowerFaceAction.argtypes = [c_void_p]

IS_FacialExpressionGetLowerFaceActionPower = \
    libEDK.IS_FacialExpressionGetLowerFaceActionPower
IS_FacialExpressionGetLowerFaceActionPower.restype = c_float
IS_FacialExpressionGetLowerFaceActionPower.argtypes = [c_void_p]

IS_MentalCommandGetCurrentAction = libEDK.IS_MentalCommandGetCurrentAction
IS_MentalCommandGetCurrentAction.restype = c_int
IS_MentalCommandGetCurrentAction.argtypes = [c_void_p]

IS_MentalCommandGetCurrentActionPower = \
    libEDK.IS_MentalCommandGetCurrentActionPower
IS_MentalCommandGetCurrentActionPower.restype = c_float
IS_MentalCommandGetCurrentActionPower.argtypes = [c_void_p]

IS_GetWirelessSignalStatus = libEDK.IS_GetWirelessSignalStatus
IS_GetWirelessSignalStatus.restype = c_int
IS_GetWirelessSignalStatus.argtypes = [c_void_p]

IS_GetContactQuality = libEDK.IS_GetContactQuality
IS_GetContactQuality.restype = c_int
IS_GetContactQuality.argtypes = [c_void_p, c_int]


class EEG(threading.Thread):

    CONTROLPANEL = c_uint(3008)
    FORWARD = 2
    BACKWARD = 4
    TURN_AMOUNT = 30
    SPEED_INC = 20

    batteryLevel     = c_long(0)
    batteryLevelP    = pointer(batteryLevel)
    maxBatteryLevel  = c_int(0)
    maxBatteryLevelP = pointer(maxBatteryLevel)
    wirelessStrength = c_int(0)
    channels = [3,7,9,12,16]
    
    def __init__(self, data):
        print "init"
        threading.Thread.__init__(self)
        self.data = data
        self.data.EEG.speed = 0
        self.data.EEG.curCommand = "neutral"
        
        # initiates robot
        self.robot = create.Create("COM4")
        # Connects to the control panel
        libEDK.IEE_EngineRemoteConnect("127.0.0.1", EEG.CONTROLPANEL)
        self.eEvent = IEE_EmoEngineEventCreate()
        self.eState = IEE_EmoStateCreate()
        self.batteryLevel     = c_long(0)
        self.batteryLevelP    = pointer(self.batteryLevel)
        self.maxBatteryLevel  = c_int(0)
        self.maxBatteryLevelP = pointer(self.maxBatteryLevel)
        self.wirelessStrength = c_int(0)
        self.channels = [3,7,9,12,16]
        
    def run(self):
        while (1):
            if (self.data.mode != "wheelchair"):
                break
            if (self.data.EEG.voiceCommand == "exit"):
                break
            state = libEDK.IEE_EngineGetNextEvent(self.eEvent)
            if state == 0:
                eventType = libEDK.IEE_EmoEngineEventGetType(self.eEvent)
                if eventType == 64:
                    libEDK.IEE_EmoEngineEventGetEmoState(self.eEvent, self.eState)

                    signalStrength = libEDK.IS_GetWirelessSignalStatus(self.eState)
                    if (signalStrength > 2):
                        self.data.EEG.signal = "Strong"
                    elif (signalStrength > 0):
                        self.data.EEG.signal = "Medium"
                    else:
                        self.data.EEG.signal = "Very weak"

                    libEDK.IS_GetBatteryChargeLevel(self.eState, self.batteryLevelP, self.maxBatteryLevelP)
                    if (self.batteryLevel.value >= 1):
                        self.data.EEG.battery = "High"
                    else:
                        self.data.EEG.battery = "Low"
                        
                    contactSum = 0;
                    for i in self.channels:
                        contactSum += IS_GetContactQuality(self.eState, i)
                    contactQuality = contactSum / len(self.channels)
                    if (contactQuality >= 3):
                        self.data.EEG.contact = "Good"
                    elif(contactQuality >= 2):
                        self.data.EEG.contact = "Medium"
                    else:
                        self.data.EEG.contact = "Bad"

                    if (self.data.EEG.voiceCommand != "stop"):
                        mentalState = IS_MentalCommandGetCurrentAction(self.eState)
                        
##                        if mentalState == EEG.FORWARD:
##                            self.data.EEG.curCommand = "forward"
##                            self.data.EEG.speed += EEG.SPEED_INC
##                            self.robot.move(self.data.EEG.speed)
                        if IS_FacialExpressionIsLeftWink(self.eState) != 0:
                            self.data.EEG.curCommand = "left"
                            self.robot.turn(EEG.TURN_AMOUNT)
                        elif IS_FacialExpressionIsRightWink(self.eState) != 0:
                            self.data.EEG.curCommand = "right"
                            self.robot.turn(-EEG.TURN_AMOUNT)
##                        elif mentalState == EEG.FORWARD:
##                            self.data.EEG.curCommand = "forward"
##                            self.data.EEG.speed += EEG.SPEED_INC
##                            self.robot.move(self.data.EEG.speed)
                        else:
                            self.data.EEG.curCommand = "neutral"

                    # Maybe try to make this part all if's instead of elif
                        
                    
            elif state != 0x0600:
                print "Internal error in Emotiv Engine ! "
                break
                
            time.sleep(0.1)

        # close connections
        libEDK.IEE_EngineDisconnect()
        libEDK.IEE_EmoStateFree(self.eState)
        libEDK.IEE_EmoEngineEventFree(self.eEvent)
        quit()




