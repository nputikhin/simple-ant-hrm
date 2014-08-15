import socket
import time

class SensorTCPServer:
    '''
    Server for Galileo with connected ANT HRM
    '''

    def startServer(self, serverAddr, handler):
        '''
        Open a new socket and bind it to serverAddr
        '''
        self.handler = handler
        self.socket = socket.socket()
        self.socket.bind(serverAddr)
        self.socket.listen(1)
        self._shutdown_request = False
    
    def waitForConnection(self):
        '''
        Wait until client connects and then create files for sending and receiving data
        '''
        if self.socket is not None:
            self.connection, self.clientAddr = self.socket.accept()
            self.rfile = self.connection.makefile("rb", 0)
            self.hasConnection = True
            
    def loop(self):
        '''
        Server loop which reads data and passes it for further processing
        '''
        while not self._shutdown_request:
            try:
                data = self.rfile.readline().strip().decode()
                if (len(data) != 0):
                    self._process(data)
                time.sleep(0.01)
            except socket.error as e:
                print("socket error:", e)
                self.shutdown()
                break
        self._onLoopShutdown()
            
        
    def shutdown(self):
        '''
        Set shutdown request for loop to stop execution on next iteration
        '''
        self._shutdown_request = True

    def _onLoopShutdown(self):
        '''
        Shutdown connection and close socket
        '''
        if self.hasConnection:
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            self.hasConnection = False
            self.rfile = None
        self.socket.close()
        self.socket = None
        
    def _process(self, data):
        '''
        Determine message type and pass it to handler for processing
        Message format:
        'type:message'
        '''
        split = data.split(":")
        msgType = split[0]
        msg = split[1]
        print("incoming message; type: {0} msg: {1}".format(msgType, msg))
        if msgType == "measure":
            self.handler.processMeasure(msg)
        elif msgType == "problem":
            self.handler.processProblem(msg)