class Utility:
    def __init__(self,logger):
        self.logger = logger
        logger.info("Initializing Utility")
    def convertBytesToGB(self,bytes):
        import math
        return math.ceil(bytes/10**9)
    def valid_threshold(self,threshold, min=1, max=100):
        if threshold < min or threshold > max:
            print("Invalid threshold", end="\n\n")
            return False
        return True