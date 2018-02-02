import wpilib
from wpilib import RobotDrive, Spark, DoubleSolenoid

class OperateGrabber:

    myDrive = RobotDrive
    grabber = DoubleSolenoid

    def __init__(self):
        self.openGrabber = False
        self.closeGrabber = False

    def setGrabber(self, openGraber, closeGrabber):
        self.openGrabber = openGrabber
        self.closeGrabber = closeGrabber

    def execute(self):
        if openGraber and not closeGrabber:
            grabber.set(DoubleSolenoid.Value.kForward)
        else:
            grabber.set(DoubleSolenoid.Value.kReverse)
