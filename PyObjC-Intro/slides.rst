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
- Interface Builder
- Objective-C Primer
- Crossing the Bridge
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

.. -*- XXX: Show Cocoa Apps -*-
.. -*- SubEthaEdit -*-
.. -*- Delicious Library -*-
.. -*- NetNewsWire -*-

Interface Builder
-----------------

- Design your interface
- ... using a well designed interface
- Don't write so much code
- Plug objects together
- Manages an *object graph*
- ... think pickle

.. -*- XXX: Demonstrate web browser building -*-

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

.. -*- XXX: Image of @interface -*-
.. -*- XXX: Image of @implementation -*-

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
- Selector
- Arguments
- nil receives anything

Exceptions
----------

- Exceptions are exceptional
- Expect bad code to just crash
- ... even from Python

Crossing the Bridge
-------------------

- All NSString are *UNICODE*
- str is not safely bridged to anything!
- int, long, float work magically
- ... for value and object types
- None is just like nil
- ... except you can't send messages to it!

Bridged Messaging
-----------------

Objective-C:
    ``[aMutableArray addObject:@"someObject"]``

- Separate the selector:from the:arguments
- Smash_the_colons\_
- Ditch.the_brackets_(and, add, arguments)

Python:
    ``aMutableArray.addObject_(u'someObject')``

Key-Value Coding
----------------

- Kinda like ``getattr`` protocol
- Accessor
- ivar
- valueForUndefinedKey: (like ``__getattr__``)

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

ConverterAppDelegate Class
--------------------------

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

    ConverterAppDelegate.setKeys_triggerChangeNotificationsForDependentKey_(
        [u'dollarsToConvert', u'exchangeRate'],
        u'amountInOtherCurrency',
    )

Converter script
----------------

::

    from PyObjCTools import AppHelper
    import ConverterAppDelegate
    if __name__ == '__main__':
        AppHelper.runEventLoop()

setup.py script
---------------

::

    from distutils.core import setup
    import py2app
    setup(
        app = ['Converter.py'],
        data_files = ['MainMenu.nib'],
    )

Build and Run
-------------

::

    % python setup.py py2app --alias
    % open dist/Converter.app

Finished Converter
------------------

.. image:: ../img/Converter/ConverterScreenSnapz001.png

Changing Currency
-----------------

.. image:: ../img/Converter/ConverterScreenSnapz002.png

Password Viewer
---------------

.. -*- XXX: Password Viewer Tutorial -*-

Help!
-----

- Documentation
- Examples
- Mailing List
- Wiki
- IRC

Applications Using PyObjC
-------------------------

- ReSTedit
- Flame
- DrawBot
- BitTorrent
- ...

Questions?
----------

**Go ahead, ask.**
