Introduction to PyObjC
----------------------

Author
    Bob Ippolito

Conference
    PyCon DC, March 2005

Intended Audience
-----------------

- Python developers using Mac OS X 10.3 or later
- ... that aren't (very) afraid of C

Topics
------

- Categories and Protocols
- Wrapping Frameworks
- ctypes?
- Writing Plug-Ins
- Code Injection
- PyObjC guts

Objective-C Tricks
------------------

- Categories
- ... think mix-in
- Protocols
- ... think interface

Categories
----------

- Used to add specific functionality to a class
- ... after it was created
- For example, AppKit adds drawing code to Foundation classes
- ... can be used to replace functionality

Creating a Category
-------------------

::

    from Foundation import *
    import objc

    >>

Questions?
----------

**Go ahead, ask.**
