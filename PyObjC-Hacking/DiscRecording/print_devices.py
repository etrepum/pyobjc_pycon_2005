from DiscRecording import *
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
for device in DRDevice.devices():
    print device.displayName()
