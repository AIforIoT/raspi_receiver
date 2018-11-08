#!/usr/bin/python3
from flask import Flask, request
import numpy as np
import struct
#from data_request_object import FrameData
import xmlrpc.client 

app = Flask(__name__)

BUFFER_MAX_SIZE = 16000  # Size of the buffer (To be changed)
BUFFER_CMD_MAX_SIZE = 64000  # Size of the buffer that will save the whole audio. (To be changed)

# Declare buffers
buffersDict = dict()
positionsDict = dict()
commandsBufferDict = dict()
commandsPositionDict = dict()

keyword_found = False


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/audio/<ide>/<delay>/<timestamp>', methods=['POST'])
def get_audio(ide, delay, timestamp):
    """
    ESP32 is sending us audio buffer!

    :param ide: Id of the ESP32.
    :param delay: Delay between bitcon and sound detected.
    :param timestamp:
    :return: 200 OK
    """
    if ide not in buffersDict:
        buffersDict[ide] = np.ndarray([BUFFER_MAX_SIZE])
        positionsDict[ide] = 0

    if not keyword_found:  # No keyword detected yet, fill up the buffer and send it to the keyword spotting module
        data = request.data.split(b',')
        for d in data:
            byte = 0
            try:
                byte = int(d)
            except:
                print("Error.... byte not int")
            buffersDict[ide][int(positionsDict[ide])] = byte
            positionsDict[ide] += 1
            if positionsDict[ide] >= BUFFER_MAX_SIZE:
                # Noise attenuation of some kind?
                # KeyWord Spotting
                #print("Keyword spotting")
                #print(buffersDict[ide])
                to_send = FrameData(np.array2string(buffersDict[ide]), '0', ide, delay, 'None', str(positionsDict[ide]), timestamp)
                client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
                client.hello(to_send)

                # Truncate
                buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
                positionsDict[ide] = int(BUFFER_MAX_SIZE / 2)
                #print(positionsDict[ide])

    else:
        # Speech to text? -> Other buffer
        if ide not in commandsBufferDict:
            commandsBufferDict[ide] = np.ndarray([BUFFER_CMD_MAX_SIZE])
            commandsPositionDict[ide] = 0

        data = request.data.split(b',')
        for d in data:
            byte = 0
            try:
                byte = int(d)
            except:
                print("Error.... byte not int")
            
            commandsBufferDict[ide][int(commandsPositionDict[ide])] = byte
            commandsPositionDict[ide] += 1
            
            if commandsPositionDict[ide] == BUFFER_CMD_MAX_SIZE:  # The buffer can overflow here!!
                print("BUG! Buffer is full! Exiting 'for' statement to not crash")
                break

    print(positionsDict[ide])
    print(buffersDict[ide])
    return "200"


@app.route('/audio/<ide>/<delay>/<timestamp>', methods=['GET'])
def end_sending(ide, delay, timestamp):
    """
    The tx was ended, its time to speech recognition!
    For esp32 speech buffer calculate the one with more power and send it to the speech recognition engine.

    :param ide: ESP32 ID
    :param delay: Delay between bitcon and sound detected.
    :param timestamp: A TimeStamp
    :return: 200 OK ot 500 Error
    """
    print("End of transmision for {} with delay: {}".format(ide, delay))
    if commandsPositionDict[ide] is not 0:
        print("End sending cmd")
	to_send = FrameData(np.array2string(commandsBufferDict[ide]), '1', ide, delay, 'None', str(commandsPositionDict[ide]), timestamp)
        client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
        client.hello(to_send)

    keyword_found = False
    commandsPositionDict[ide] = 0
    positionsDict[ide] = 0
    return 200


@app.route('/keyword_detected', methods=['GET'])
def keyword_detector():
    keyword_found = True
    return 200


# TODO
def is_voice(ide):
    """
    Decides if the rx buffer is voice or not

    :param ide: ide of the ESP32, to identify the buffer
    :return: Boolean -> is voice?
    """
    print(ide)
    return True


if __name__ == '__main__':
    app.run()
