import socket
import time

import hrm

class SensorTCPClient:
    '''
    Client that runs on Galileo with connected ANT HRM
    '''
        
    def connectToServer(self, serverAddr):
        '''
        Connect to serverAddr
        '''
        self.socket = socket.socket()
        self.socket.connect(serverAddr)
        self.wfile = self.socket.makefile("wb", 0)
        self.hasConnection = True

    def shutdown(self):
        '''
        Shutdown connection and close socket
        '''
        if self.hasConnection:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.hasConnection = False
            self.wfile = None
        self.socket.close()
        self.socket = None
        
    def sendMeasure(self, measure):
        '''
        Send measure to server
        Measure format:
        '[HR] [BC]' where HR is heart rate and BC is beat count
        '''
        self._send("measure:{}".format(measure))
        
    def sendProblem(self, problem):
        '''
        Send problem to server
        '''
        self._send("problem:{}".format(problem))
        
    def _send(self, string):
        '''
        Send string to server
        '''
        if self.hasConnection:
            try:
                print "sending {}".format(string)
                self.wfile.write("{}\n".format(string).encode())
            except socket.error as e:
                print "socket error:", e
                self.hasConnection = False
                self.shutdown()

if __name__ == '__main__':
    client = SensorTCPClient();
    client.connectToServer(("169.254.211.109", 4004))
    shutdown = False

    monitor = hrm.HRM(client)
    monitor.start()
    monitor.launchHRMChannel()

    while client.hasConnection:
        time.sleep(1)

    monitor.shutdown()