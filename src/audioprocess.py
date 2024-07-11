import qi
import argparse
import sys
import time
import numpy as np
import socket


class SoundProcessingModule(object):
    def __init__(self,app,client_socket):
        super(SoundProcessingModule, self).__init__()
        app.start()
        session = app.session
        # Get the service ALAudioDevice.
        self.audio_service = session.service("ALAudioDevice")
        self.isProcessingDone = True
        self.framesCount=0
        self.micFront = []
        self.module_name = "SoundProcessingModule"
        
        self.singal=0 # 0 is stop(default),1 is ready, 2 is start, 3 is exit.
        self.isSubscribe = 0
        self.client_socket = client_socket

    def startProcessing(self):
        """
        Start processing
        """
        while True:
            # Stop waiting for user signal
            self.singal = self.client_socket.recv(1)
            if self.singal is None or self.singal == '':
                self.singal = 0
                continue
            if self.singal == 0 and self.isSubscribe == 1:
                self.audio_service.unsubscribe(self.module_name)
                self.isProcessingDone = True
                self.isSubscribe = 0
            if self.singal == 0 and self.isSubscribe == 0:
                self.isProcessingDone = True
            if self.singal == 1:
                # ask for the front microphone signal sampled at 16kHz
                # if you want the 4 channels call setClientPreferences(self.module_name, 48000, 0, 0)
                self.audio_service.setClientPreferences(self.module_name, 16000, 3, 0)
                self.audio_service.subscribe(self.module_name)
                self.isSubscribe = 1
            if self.singal == 2:
                self.isProcessingDone = False
            if self.singal == 3:
                self.audio_service.unsubscribe(self.module_name)
                break
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
    singal_socket.bind((args.socketip, args.socketport))
    singal_socket.listen(1)
    client_socket, addr = singal_socket.accept()
    
    MySoundProcessingModule = SoundProcessingModule(app,client_socket)
    app.session.registerService("SoundProcessingModule", MySoundProcessingModule)
    MySoundProcessingModule.startProcessing()
    client_socket.close()