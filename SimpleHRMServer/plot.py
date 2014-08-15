'''
Loosely based on animate_decay example of matplotlib
http://matplotlib.org/examples/animation/animate_decay.html
'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class Plotter:
    '''
    This class builds plots using matplotlib
    '''
    # Heart rates array to use as y values for plot
    heartRates = [0]
    # Times array (in seconds passed) to use as x values for plot
    times = [0]
    
    # Default borders 
    defaultYmin = 60
    defautYmax = 120
    
    # This is used when borders shift
    yLimStep = 10
    
    # This is threshold for border shift
    yLimThreshold = 5
    
    # This is range of plot in seconds
    # Plot is displayed from time - xRange to time + xRange
    xRange = 10
    
    def __init__(self, handler):
        # HRMHandler is used as data source
        self.handler = handler
        
        # Create subplot with red line
        self.figure, self.axes = plt.subplots()
        self.line, = self.axes.plot([], [], color='red')
        
        # Label axes
        plt.ylabel("Heart rate")
        plt.xlabel("Seconds")
        
        # Set default limits
        self.axes.set_ylim(self.defaultYmin, self.defautYmax)
        self.axes.set_xlim(-self.xRange, self.xRange)
        
    def animate(self, interval):
        '''
        Launches animation
        NOTE: this function does not display plot window, to do it call getPlot().show()
        '''
        self.startTime = time.time()
        self.animation = animation.FuncAnimation(self.figure, self._iteration, blit=True, interval=interval)
        
    def getPlot(self):
        return plt
    
    def _iteration(self, discarded):
        '''
        This function is called by animation.FuncAnimation
        '''
        rate = self.handler.heartRate
        
        # Heart rate is used as a value
        self.heartRates.append(rate)
        self.line.set_ydata(self.heartRates)
        
        # Seconds passed from the beginning are used as a value
        currentTime = time.time() - self.startTime
        self.times.append(currentTime)
        self.line.set_xdata(self.times)
        
        # Plot X borders move every step
        self.axes.set_xlim(currentTime - self.xRange, currentTime + self.xRange)
        self.axes.figure.canvas.draw()
        
        # Shift Y borders if value is near limits
        
        ymin, ymax = self.axes.get_ylim()
        
        if ymin >= rate - self.yLimThreshold:
            self.axes.set_ylim(ymin - self.yLimStep, ymax - self.yLimStep)
            self.axes.figure.canvas.draw()
            
        if ymax <= rate + self.yLimThreshold:
            self.axes.set_ylim(ymin + self.yLimStep, ymax + self.yLimStep)
            self.axes.figure.canvas.draw()
                
        return self.line,