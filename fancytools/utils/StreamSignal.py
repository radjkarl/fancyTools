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

    def flush(self):
        pass #to prevent errors for sys.stdout.flush()




if __name__ == '__main__':
    import sys
    # create connectable stdout and stderr signal:
    streamOut = StreamSignal()
    streamErr = StreamSignal()
    # save the std output funcs:
    stdoutW = sys.stdout.write
    stderrW = sys.stderr.write
    # forward the std-signals to the new ones:
    sys.stdout = streamOut
    sys.stderr = streamErr
    #reconnect sysout to the qtSignal:
    streamOut.message.connect(stdoutW)
    streamErr.message.connect(stderrW)