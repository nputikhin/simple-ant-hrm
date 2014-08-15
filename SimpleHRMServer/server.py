import threading

import sensorserver

from plot import Plotter

class HRMHandler:
    '''
    This class handles messages for server and saves information about heart rate
    '''
    
    # Last successfully measured heart rate
    heartRate = 0
    
    def processMeasure(self, measure):
        # Measure format is '[HR] [BC]' where HR is heart rate and BC is beat count
        heartRate = int(measure.split()[0])
        beatCount = int(measure.split()[1])
        print("HR: {0} BC: {1}".format(heartRate, beatCount))
        self.heartRate = heartRate
        
    def processProblem(self, problem):
        print("Problem:", problem)

if __name__ == '__main__':
    handler = HRMHandler()
    server = sensorserver.SensorTCPServer()

    print("Starting server and waiting for connection")
    server.startServer(('', 4004), handler)
    server.waitForConnection()
    
    print("Starting loop")
    server_thread = threading.Thread(target = server.loop)
    server_thread.daemon = True
    server_thread.start()
    
    plotter = Plotter(handler)
    plotter.animate(20)
    
    plotter.getPlot().show()
    # Execution continues after user closes the window
        
    print("Shutting down")
    server.shutdown()