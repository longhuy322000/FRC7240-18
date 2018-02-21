from wpilib import DoubleSolenoid

class OperateGrabber:

    grabber1 = DoubleSolenoid

    def __init__(self):
        self.option = False

    def setGrabber(self, option):
        self.option = option

    def execute(self):
        if self.option:
            self.grabber1.set(DoubleSolenoid.Value.kForward)
        else:
            self.grabber1.set(DoubleSolenoid.Value.kReverse)
