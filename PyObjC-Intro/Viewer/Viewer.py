from PyObjCTools import AppHelper
from Foundation import *
from AppKit import *
import os

FIELDS = """
user password uid gid class change
expire gecos home_dir shell
""".split()

class ViewerAppDelegate(NSObject):
    def init(self):
        self = super(ViewerAppDelegate, self).init()
        self.passwords = [
            dict(zip(FIELDS, line.rstrip().split(':')))
            for line in os.popen('/usr/bin/nidump passwd .')
            if line and not line.startswith('#')
        ]
        return self

if __name__ == '__main__':
    AppHelper.runEventLoop()
