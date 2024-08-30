import qi
import argparse
import sys
import time
import numpy as np
import socket


class SoundProcessingModule(object):
    def ledsOn(self):
        global isLedsOn
        self.isLedsOn = True
        # leds.rotateEyes(0xFFF00, 1, 15, _async=True)
        self.leds.fadeRGB('FaceLeds', 0, 1, 0, 0.1)
    def __init__(self,app,client_socket):
        super(SoundProcessingModule, self).__init__()
        app.start()
        session = app.session
        # Get the service ALAudioDevice.
        self.audio_service = session.service("ALAudioDevice")
        self.leds_service = session.service("ALLeds")
        self.ledsOn = False
        self.isProcessingDone = True
        self.framesCount=0
        self.micFront = []
        self.module_name = "SoundProcessingModule"
        
        self.singal=0 # 0 is default,1 is start, 2 is stop, 3 is exit.
        self.isSubscribe = 0
        self.client_socket = client_socket
    def startProcessing(self):
        """
        Start processing
        """
        while True:
            # Stop waiting for user signal
            self.singal = self.client_socket.recv(1)
            
            if self.singal == b'1':
                # ask for the front microphone signal sampled at 16kHz
                # if you want the 4 channels call setClientPreferences(self.module_name, 48000, 0, 0)
                self.audio_service.setClientPreferences(self.module_name, 16000, 3, 0)
                self.audio_service.subscribe(self.module_name)
                self.isProcessingDone = False
                if not isLedsOn:
                    self.ledsOn()
                    self.isLedsOn = True
                self.singal == b'0'
                
            elif self.singal == b'2':
                self.isProcessingDone = True
                if isLedsOn:
                    self.leds.reset('FaceLeds')
                    self.isLedsOn = False
                self.audio_service.unsubscribe(self.module_name)
                self.singal == b'0'
                
            elif self.singal == b'3':
                self.audio_service.unsubscribe(self.module_name)
                self.singal == b'0'
                break
            else:
                pass
        return 1
    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        if self.isProcessingDone == False:
            self.client_socket.sendall(inputBuffer)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--socketip", type=str, default='0.0.0.0',
                        help="Naoqi port number")
    parser.add_argument("--socketport", type=int, default=12345,
                        help="Naoqi port number")
    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["SoundProcessingModule", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    
    singal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    singal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    singal_socket.bind((args.socketip, args.socketport))
    singal_socket.listen(1)
    client_socket, addr = singal_socket.accept()
    isFinish=0
    while isFinish==0:
        try:
            MySoundProcessingModule = SoundProcessingModule(app,client_socket)
            app.session.registerService("SoundProcessingModule", MySoundProcessingModule)
            isFinish=MySoundProcessingModule.startProcessing()
        # except BrokenPipeError:
        #     client_socket, addr = singal_socket.accept()
        except KeyboardInterrupt:
            isFinish=1
            break

    client_socket.close()