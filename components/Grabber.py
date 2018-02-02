import wpilib
from wpilib import RobotDrive, Spark, DoubleSolenoid

class DriveTrain:

    myDrive = RobotDrive
    grabber = DoubleSolenoid

    def __init__(self):
        self.inTake = False
        self. = False

    def move(self, powerLeft, powerRight):
        self.powerLeft = powerLeft
        self.powerRight = powerRight

    def execute(self):
        self.myDrive.tankDrive(self.powerLeft, self.powerRight)
