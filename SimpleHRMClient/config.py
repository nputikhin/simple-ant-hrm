from ant.core import log

# USB1 ANT stick interface. Running `dmesg | tail -n 25` after plugging the
# stick on a USB port should tell you the exact interface.
SERIAL = '/dev/ttyUSB0'

# If set to True, the stick's driver will dump everything it reads/writes
# from/to the stick.
DEBUG = False

# Set to None to disable logging
LOG = None
#LOG = log.LogWriter()

# ========== DO NOT CHANGE ANYTHING BELOW THIS LINE ==========
if LOG is not None:
	print "Using log file:", LOG.filename
	print ""
