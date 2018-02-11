from wpilib import drive

class AutoDrive:

    myDrive = drive.DifferentialDrive

    def __init__(self):
        self.power = 0
        self.angle = 0

    def move(self, power, angle):
        self.power = power
        self.angle = angle

    def execute(self):
        self.myDrive.arcadeDrive(self.power, self.angle)
