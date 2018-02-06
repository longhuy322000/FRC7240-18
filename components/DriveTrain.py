import wpilib
from wpilib import RobotDrive, drive

class DriveTrain:

    myDrive = drive.DifferentialDrive

    def __init__(self):
        self.powerLeft = 0
        self.powerRight = 0

    def move(self, powerLeft, powerRight):
        self.powerLeft = powerLeft
        self.powerRight = powerRight

    def execute(self):
        self.myDrive.tankDrive(self.powerLeft, self.powerRight)
