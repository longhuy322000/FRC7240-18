from wpilib import drive

class DriveTrain:

    myDrive = drive.DifferentialDrive

    def __init__(self):
        self.powerLeft = 0
        self.powerRight = 0
        self.STICK_DEADBAND = 0.005
        self.CENTER = 0.0

    def moveAuto(self, powerLeft, powerRight):
        self.powerLeft = powerLeft
        self.powerRight = powerRight

    def moveTelo(self, powerLeft, powerRight):
        def stickDeadband(self, value):
            if value < (self.CENTER + self.STICK_DEADBAND) and value > (self.CENTER - self.STICK_DEADBAND):
                return value
            return self.CENTER
        self.powerLeft = stickDeadband(powerLeft)
        self.powerRight = self.stickDeadband(powerRight)

    def execute(self):
        self.myDrive.tankDrive(self.powerLeft, self.powerRight)
