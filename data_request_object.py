import os

'''
The object FrameData must contain all the information about a frame. 
The ConfigParams object must contain the following information: esp_id, delay, power and offset. All this 
values must be stored as string.
The numpy_data object must be a numpy object formatted as string and it contains the data form voice.
'''


class ConfigParams:
    __esp_id: object
    __delay: object
    __power: object
    __offset: object

    def __init__(self, esp_id, delay, power, offset):
        self.esp_id = esp_id
        self.delay = delay
        self.power = power
        self.offset = offset


    @property
    def esp_id(self):
        return self.__esp_id

    @esp_id.setter
    def esp_id(self, val):
        self.__esp_id = val

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, val):
        self.__delay = val

    @property
    def power(self):
        return self.__power

    @power.setter
    def power(self, val):
        self.__power = val

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, val):
        self.__offset = val

class FrameData:
    __numpy_data = object
    __config_params = object

    def __init__(self, numpy_data, esp_id, delay, power, offset):
        self.numpy_data = numpy_data
        self.config_params = ConfigParams(esp_id, delay, power, offset)


    @property
    def numpy_data(self):
        return self.__numpy_data

    @numpy_data.setter
    def numpy_data(self, val):
        self.__numpy_data = val

    @property
    def config_params(self):
        return self.__config_params

    @config_params.setter
    def config_params(self, val):
        self.__config_params = val


