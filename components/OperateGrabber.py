from wpilib import DoubleSolenoid

class OperateGrabber:

    grabber = DoubleSolenoid

    def __init__(self):
        self.option = False

    def setGrabber(self, option):
        self.option = option

    def execute(self):
        print(self.option)
        if self.option:
            self.grabber.set(DoubleSolenoid.Value.kForward)
        else:
            self.grabber.set(DoubleSolenoid.Value.kReverse)
