import numpy as np
from data_request_object import FrameData
import xmlrpc.client

from scipy.io.wavfile import read
a = read("./Iouti.wav")

buff = np.array(a[1], dtype=float)
ide = str(3)
delay = str(432)
pos = str(50)
timestamp = str(1540196375000)


to_send = FrameData(np.array2string(buff), '0', ide, delay, 'None', pos, timestamp)
client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
client.hello(to_send)
