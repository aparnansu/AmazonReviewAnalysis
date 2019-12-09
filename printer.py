from abc import ABC, abstractmethod 

class Printer(ABC):
                   
    def print(self, msg):
        pass

    # Release any resources
    def close(self):
        pass
