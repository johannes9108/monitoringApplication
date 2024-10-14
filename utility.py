'''
Module that contains utility functions for the monitoring application
'''
import math
import ui
from customlogger import logger as importLogger
class Utility:
    '''
    Class that contains utility functions for the monitoring application
    '''
    def __init__(self):
        pass
    @staticmethod
    def convertBytesToGB(totalBytes):
        '''
        Converts bytes to gigabytes
        '''
        return math.ceil(totalBytes/10**9)
    @staticmethod
    def validThreshold(threshold, minValue=1, maxValue=100):
        '''
        Compares the threshold to the min and max values
        '''
        if threshold < minValue or threshold > maxValue:
            print("Invalid threshold", end="\n\n")
            return False
        return True
    @staticmethod
    def output(*texts, console, logger,level=20,sep=" ",end="\n"):
        '''
        Prints a simple string message to both/or console and logger
        '''
        
        if console :
            ui.UI.print(*texts,sep=sep,end=end)
        if logger :
            for text in texts:
                message = text.replace(" ","_")
                importLogger.log(level,message)
