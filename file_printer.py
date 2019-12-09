from printer import Printer

class FilePrinter(Printer):

    def __init__(self, fileName):
        self.fileName = fileName;        
        self.printer = open(fileName, 'w')
        print('File report opened for', self.fileName)
        
    def print(self, msg):
        self.printer.write(msg + '\n')        

    def close(self):
        self.printer.close()
        print('File report closed for', self.fileName)
        return
