'''
Created on 6 Jul 2014

@author: elkb4
'''
from PyQt4 import QtCore

class StreamSignal(QtCore.QObject):
    '''
    TODO
    '''
    #message = QtCore.Signal(str)# works under pyside
    message = QtCore.pyqtSignal(str)

    def __init__(self, logFile=None, parent=None):
        super(StreamSignal, self).__init__(parent)

    def write(self, message):
        self.message.emit(message)



if __name__ == '__main__':
    #TODO
    pass