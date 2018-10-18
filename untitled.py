from flask import Flask, request
import numpy as np

app = Flask(__name__)

BUFFER_MAX_SIZE = 512  # Size of the buffer (To be changed)
BUFFER_CMD_MAX_SIZE = 1024  # Size of the buffer that will save the whole audio. (To be changed)

# Declare buffers
buffersDict = dict()
positionsDict = dict()
commandsBufferDict = dict()
commandsPositionDict = dict()

keyword_found = False


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@app.route('/<ide>', methods=['POST'])
def get_audio(ide):
    """
    ESP32 is sending us audio buffer!

    :param ide: Id of the ESP32.
    :return: 200 OK
    """
    if ide not in buffersDict:
        buffersDict[ide] = np.ndarray([BUFFER_MAX_SIZE])
        positionsDict[ide] = 0

    if not keyword_found:  # No keyword detected yet, fill up the buffer and send it to the keyword spotting module
        for byte in request.data:
            buffersDict[ide][positionsDict[ide]] = byte
            positionsDict[ide] += 1
            if positionsDict[ide] >= BUFFER_MAX_SIZE:
                # Noise attenuation of some kind?
                if is_voice(ide):
                    # KeyWord Spotting - Problem: wait for this module to respond is thread blocking
                    pass

                # Truncate
                buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
                positionsDict[ide] = BUFFER_MAX_SIZE / 2
    else:
        # Speech to text? -> Other buffer
        if ide not in commandsBufferDict:
            commandsBufferDict[ide] = np.ndarray([BUFFER_CMD_MAX_SIZE])
            commandsPositionDict[ide] = 0

        for byte in request.data:
            if commandsPositionDict[ide] == BUFFER_CMD_MAX_SIZE:  # The buffer can overflow here!!
                print("BUG! Buffer is full! Exiting 'for' statement to not crash")
                break
            commandsBufferDict[ide][commandsPositionDict[ide]] = byte
            commandsPositionDict[ide] += 1

    return 200


@app.route('/<ide>/<delay>/', methods=['GET'])
def end_sending(ide, delay):
    """
    The tx was ended, its time to speech recognition!
    For esp32 speech buffer calculate the one with more power and send it to the speech recognition engine.

    :param ide: ESP32 ID
    :param delay: Timestamp (for localization purpose)
    :return: 200 OK ot 500 Error
    """
    print("End of transmision for {} with delay: {}".format(ide, delay))
    if commandsPositionDict[ide] is not 0:
        # TODO: Send commandBufferDict[ide][0:commandsPositionDict[ide]] to speech to text module.
        # Maybe only if ide is the choosen one
        pass
    keyword_found = False
    commandsPositionDict[ide] = 0
    positionsDict[ide] = 0
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
