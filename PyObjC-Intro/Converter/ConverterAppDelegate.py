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
