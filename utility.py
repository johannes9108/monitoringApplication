'''
Module that contains utility functions for the monitoring application
'''
import math

class Utility:
    '''
    Class that contains utility functions for the monitoring application
    '''
    def __init__(self,logger):
        self.logger = logger
        logger.info("Initializing Utility")
    def convertBytesToGB(self,totalBytes):
        '''
        Converts bytes to gigabytes
        '''
        return math.ceil(totalBytes/10**9)
    def validThreshold(self,threshold, minValue=1, maxValue=100):
        '''
        Compares the threshold to the min and max values
        '''
        if threshold < minValue or threshold > maxValue:
            print("Invalid threshold", end="\n\n")
            return False
        return True
    def output(self,message, console, logger,end="\n"):
        '''
        Prints a simple string message to both/or console and logger
        '''
        if console :
            print(message,end=end)
        if logger :
            message = message.replace(" ","_")
            self.logger.info(message)
