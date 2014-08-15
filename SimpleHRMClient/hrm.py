'''
Code mostly taken from python-ant/demos/ant.core/04-processevents.py
'''
from ant.core import driver
from ant.core import node
from ant.core import event
from ant.core import message
from ant.core.constants import *

from config import *

NETKEY = '\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

# A run-the-mill event listener
class HRMListener(event.EventCallback):
    def __init__(self, client):
        self.client = client

    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            # Beat count is msg.payload[-2]
            # Heart rate is msg.payload[-1]
            self.client.sendMeasure('{0} {1}'.format(ord(msg.payload[-1]), ord(msg.payload[-2])))
        if isinstance(msg, message.ChannelEventMessage):
            if (msg.getMessageID() == 1):
                if (msg.getMessageCode() == 2):
                    self.client.sendProblem('EVENT_RX_FAIL')
                elif (msg.getMessageCode() == 8):
                    self.client.sendProblem('EVENT_RX_FAIL_GO_TO_SEARCH')

class HRM:
    def __init__(self, client):
        self.client = client

    def start(self):
        print 'Initializing'
        # Initialize
        stick = driver.USB1Driver(SERIAL, debug=DEBUG)
        self.antnode = node.Node(stick)
        self.antnode.start()

    def launchHRMChannel(self):
        print 'Setting up the channel'
        # Setup channel
        key = node.NetworkKey('N:ANT+', NETKEY)
        self.antnode.setNetworkKey(0, key)
        self.channel = self.antnode.getFreeChannel()
        self.channel.name = 'C:HRM'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(120, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
        self.channel.setPeriod(8070)
        self.channel.setFrequency(57)
        self.channel.open()

        # Setup callback
        # Note: We could also register an event listener for non-channel events by
        # calling registerEventListener() on antnode rather than channel.
        self.channel.registerCallback(HRMListener(self.client))
        
    def shutdown(self):
        print 'Shutting down'
        # Shutdown
        self.channel.close()
        self.channel.unassign()
        self.antnode.stop()
