Introduction to PyObjC
----------------------

Author
    Bob Ippolito

Conference
    PyCon DC, March 2005

Intended Audience
-----------------

- Python developers using Mac OS X 10.3 or later
- Spies from the Linux and Win32 camps
- Hopefully a GNUstep porter/maintainer

Topics
------

- Installing PyObjC
- Why Bother?
- Objective-C Primer
- Crossing the Bridge
- Interface Builder
- Your First Application
- Help!
- Who's Using This Stuff?

Installing PyObjC
-----------------

Install Xcode:
    http://developer.apple.com/

Install PyObjC:
    http://pyobjc.sourceforge.net/

Why Bother?
-----------

- You paid for that Mac
- The tools kick ass
- Apple (often) writes good code
- The tools kick ass
- Objective-C and Python are friends

.. SubEthaEdit is Cocoa...
.. -----------------------
.. 
.. .. image:: ../img/Apps/SubEthaEdit.png
.. 
.. So is NetNewsWire...
.. --------------------
.. 
.. .. image:: ../img/Apps/NetNewsWire.png

Objective-C
-----------

- True superset of C
- Everything is not an object
- Looks kinda like Smalltalk

Classes
-------

- Flat Namespace
- Single Inheritance
- ... with Categories and Protocols
- Classes are objects
- Instance Variables

Objective-C Interface
---------------------

::

    @interface MyClass : NSObject
    {
        int myInt;
    }
    +(id)myClassWithInt:(int)anInt;
    -(int)myInt;
    @end

Objective-C Implementation
--------------------------

::

    @implementation MyClass

    +(id)myClassWithInt:(int)anInt;
    {
        self = [[self alloc] init];
        intInstanceVariable = anInt;
        return self;
    }

    -(int)myInt
    {
        return myInt;
    }

    @end
    
Objects
-------

- Separate alloc/init
- Everything is an accessor
- ... except when using Key-Value Coding
- Reference counted
- ... but we take care of that
- ... except where Apple doesn't

Messages
--------

- Target
- ... can be nil
- Selector
- Arguments

Exceptions
----------

- Exceptions are exceptional
- Expect bad code to just crash
- ... even from Python

Crossing the Bridge
-------------------

- unicode, int, long, float work magically
- ... str is not safely bridged!
- None is just like nil
- ... except you can't send messages to it!

Objective-C Messages
--------------------

Objective-C Message:
    ``[aMutableArray addObject:@"someObject"]``

Target:
    ``aMutableArray``

Selector:
    ``addObject:``

Arguments:
    ``@"someObject"``


PyObjC Messages
---------------

Python Message:
    ``aMutableArray.addObject_(u'someObject')``

Target:
    ``aMutableArray``

Selector:
    ``addObject:`` (with colons replaced by underscores!)

Arguments:
    ``u'someObject'`` (unicode is equivalent to ``@"string"``)


Key-Value Coding
----------------

- Kinda like ``getattr`` protocol
- ... but it calls accessors for you (like property)
- ... or it will fetch an ivar and convert to an object
- ``valueForUndefinedKey:`` (like ``__getattr__``)
- ``valueForKeyPath:`` looks like a Python expression
- ... except it will also "map" over arrays
- ... and can do cool things like sum

Interface Builder
-----------------

- Design your interface
- ... using a well designed interface
- Don't write so much code
- Plug objects together
- Manages an *object graph*
- ... think pickle

Making Money
------------

- Currency Converter
- Using Cocoa Bindings
- Almost entirely in Interface Builder

New Application in IB
---------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz001.png

Create an NSTextField
---------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz002.png

Drag to the NSWindow
--------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz003.png

Create the input NSTextFields
-----------------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz004.png

Almost finished UI Layout
-------------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz005.png

Align the labels
----------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz006.png

Use currency NSNumberFormatters
-------------------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz016.png

Set up the Bindings
-------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz007.png

To point to your delegate
-------------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz008.png

Dollars binding...
------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz009.png

Other Currency Binding...
-------------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz010.png

Subclass NSObject
-----------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz011.png

To create your delegate class
-----------------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz012.png

Instantiate it in your nib
--------------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz013.png

Create a connection
-------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz014.png

To the NSApplication
--------------------

.. image:: ../img/Converter/InterfaceBuilderScreenSnapz015.png

ConverterAppDelegate.py Class
-----------------------------

::

    from Foundation import *
    from AppKit import *
    import objc

    class ConverterAppDelegate(NSObject):
        def init(self):
            self = super(ConverterAppDelegate, self).init()
            self.exchangeRate = 3
            self.dollarsToConvert = 4
            return self

        def amountInOtherCurrency(self):
            return self.dollarsToConvert * self.exchangeRate

        def setAmountInOtherCurrency_(self, amt):
            self.dollarsToConvert = amt / self.exchangeRate

    # shamelessly preventing line wrapping
    cls = ConverterAppDelegate
    cls.setKeys_triggerChangeNotificationsForDependentKey_(
        [u'dollarsToConvert', u'exchangeRate'],
        u'amountInOtherCurrency',
    )

Converter.py script
-------------------

::

    from PyObjCTools import AppHelper
    import ConverterAppDelegate
    if __name__ == '__main__':
        AppHelper.runEventLoop()

Converter setup.py script
-------------------------

::

    from distutils.core import setup
    import py2app
    setup(
        app = ['Converter.py'],
        data_files = ['MainMenu.nib'],
    )

Build and Run
-------------

Build::

    % python setup.py py2app --alias

Run::

    % open dist/Converter.app

Done:


.. image:: ../img/Converter/ConverterScreenSnapz001.png

Hack the Gibson
---------------

- Views password file
- ... using ``nidump`` utility
- In a table view

New NSTableView
---------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz001.png

Name the columns
----------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz002.png

Change the resize behavior
--------------------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz003.png

To expand with the NSWindow
---------------------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz004.png

Create an NSArrayController
---------------------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz005.png

Create the ViewerAppDelegate
----------------------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz006.png

Bind the NSArrayController
--------------------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz009.png

Like the previous application:

- Subclass NSObject
- Instantiate the subclass
- Connect it to the NSApplication's delegate outlet

Bind the user column
--------------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz007.png

Bind the uid column
-------------------

.. image:: ../img/Viewer/InterfaceBuilderScreenSnapz008.png

Viewer.py
---------

::

    from PyObjCTools import AppHelper
    from Foundation import *
    from AppKit import *
    import os

    # another shameless anti-line-wrapping hack
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
            
Build and Run Viewer
--------------------

Build (redistributable!)::

    % py2applet Viewer.py MainMenu.nib

Run::

    % open Viewer.app

Done:

.. image:: ../img/Viewer/ViewerScreenSnapz001.png

Bindings give you sorting for free!
-----------------------------------

.. image:: ../img/Viewer/ViewerScreenSnapz002.png

Help!
-----

Documentation:
    /Developer/Python/PyObjC/Documentation

Examples:
    /Developer/Python/PyObjC/Examples
    
Wiki:
    http://pythonmac.org/wiki

IRC:
    #macpython (on freenode)

Mailing Lists:

- pyobjc-dev@lists.sourceforge.net
- pythonmac-sig@python.org

Help! (Objective-C)
-------------------

Documentation:
    http://developer.apple.com/

Examples:
    /Developer/Examples/AppKit
    
Wiki:
    http://cocoadev.com/

Mailing List:
    cocoa-dev@lists.apple.com

ReSTedit
--------

.. image:: ../img/Apps/ReSTedit.png

Flame
-----

.. image:: ../img/Apps/Flame.png

NodeBox
-------

.. image:: ../img/Apps/NodeBox.png

Questions?
----------

**Go ahead, ask.**
