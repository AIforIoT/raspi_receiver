import numpy as np
from data_request_object import FrameData
import xmlrpc.client 

buff = np.ndarray([320000])
ide = str(3)
delay = str(432)
pos = str(50)
timestamp = str(1540196375000)


to_send = FrameData(np.array2string(buff), ide, delay, 'None', pos, timestamp)
client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
client.hello(to_send)
