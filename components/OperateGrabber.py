from wpilib import DoubleSolenoid

class OperateGrabber:

    grabber = DoubleSolenoid

    def __init__(self):
        self.openGrabber = False
        self.closeGrabber = False

    def setGrabber(self, openGrabber, closeGrabber):
        self.openGrabber = openGrabber
        self.closeGrabber = closeGrabber

    def execute(self):
        if self.openGrabber and not self.closeGrabber:
            self.grabber.set(DoubleSolenoid.Value.kForward)
        else:
            self.grabber.set(DoubleSolenoid.Value.kReverse)
