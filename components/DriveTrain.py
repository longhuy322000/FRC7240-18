from wpilib import drive, ADXRS450_Gyro
from magicbot import tunable

class DriveTrain:

    myDrive = drive.DifferentialDrive
    kP = tunable(0.1)
    gyro = ADXRS450_Gyro

    def __init__(self):
        self.powerLeft = 0
        self.powerRight = 0
        self.power = 0
        self.STICK_DEADBAND = 0.005
        self.CENTER = 0.0
        self.option = False
        self.angle = 0

    def stickDeadband(self, value):
        if value < (self.CENTER + self.STICK_DEADBAND) and value > (self.CENTER - self.STICK_DEADBAND):
            return self.CENTER
        return value

    def moveAngle(self, power, angle):
        self.power = -power
        self.angle = self.kP * (self.gyro.getAngle() - angle)
        self.option = False

    def moveAuto(self, power, angle):
        self.power = -power
        self.angle = angle
        self.option = False

    def moveTank(self, powerLeft, powerRight):
        self.powerLeft = self.stickDeadband(powerLeft)
        self.powerRight = self.stickDeadband(powerRight)
        self.option = True

    def execute(self):
        if self.option:
            self.myDrive.tankDrive(self.powerLeft, self.powerRight)
            self.power = 0
            self.angle = 0
        else:
            self.myDrive.arcadeDrive(self.power, self.angle)
            self.power = 0
            self.angle = 0
