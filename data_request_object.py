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
    __timestamp: object


    def __init__(self, esp_id, delay, power, offset, timestamp):
        self.esp_id = esp_id
        self.delay = delay
        self.power = power
        self.offset = offset
        self.timestamp = timestamp


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

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, val):
        self.__timestamp = val


class FrameData:
    __numpy_data = object
    __config_params = object
    __data_type: object


    def __init__(self, numpy_data, data_type, esp_id, delay, power, offset, timestamp):
        self.numpy_data = numpy_data
        self.config_params = ConfigParams(esp_id, delay, power, offset, timestamp)
        self.data_type = data_type


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

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, val):
        self.__data_type = val
