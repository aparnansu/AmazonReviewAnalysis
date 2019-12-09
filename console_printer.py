from printer import Printer

class ConsolePrinter(Printer):
    
    def print(self, msg):
        print(msg)    

    def close(self):
        return
