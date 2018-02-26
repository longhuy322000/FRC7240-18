from wpilib import drive, ADXRS450_Gyro, Encoder
from magicbot import tunable

class DriveTrain:

    myDrive = drive.DifferentialDrive
    #reverseMyDrive = drive.DifferentialDrive
    leftValue = tunable(0)
    rightValue = tunable(0)
    gyro = ADXRS450_Gyro
    leftEncoder = Encoder
    rightEncoder = Encoder

    def __init__(self):
        self.powerLeft = 0
        self.powerRight = 0
        self.power = 0
        self.STICK_DEADBAND = 0.005
        self.CENTER = 0.0
        self.option = -1
        self.angle = 0
        self.kP = 0.8

    def stickDeadband(self, value):
        if value < (self.CENTER + self.STICK_DEADBAND) and value > (self.CENTER - self.STICK_DEADBAND):
            return self.CENTER
        return value

    def stopMotor(self):
        self.power = 0
        self.angle = 0
        self.option = False

    def moveAngle(self, power, angle):
        self.power = -power
        self.angle = self.kP * (self.gyro.getAngle() - angle)
        self.option = False

    def moveAuto(self, power, angle):
        self.power = -power
        self.angle = angle
        self.option = False

    def movePathFinder(self, powerLeft, powerRight):
        self.powerLeft = powerLeft
        self.powerRight = powerRight
        self.option = True

    def moveTank(self, powerLeft, powerRight):
        self.powerLeft = self.stickDeadband(powerLeft)
        self.powerRight = self.stickDeadband(powerRight)
        self.option = True

    def execute(self):
        if not self.option:
            self.myDrive.arcadeDrive(self.power, self.angle)
        else:
            self.myDrive.tankDrive(self.powerLeft, self.powerRight)
        self.power = 0
        self.powerLeft = 0
        self.powerRight = 0
        self.angle = 0
