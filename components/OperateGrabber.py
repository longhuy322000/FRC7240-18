from wpilib import DoubleSolenoid

class OperateGrabber:

    grabber = DoubleSolenoid

    def __init__(self):
        self.option = 'close'

    def setGrabber(self, option):
        self.option = option

    def execute(self):
        if self.option == 'close':
            self.grabber.set(DoubleSolenoid.Value.kForward)
        else:
            self.grabber.set(DoubleSolenoid.Value.kReverse)
