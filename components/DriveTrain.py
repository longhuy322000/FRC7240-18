from wpilib import drive, ADXRS450_Gyro, Encoder
from magicbot import tunable

class DriveTrain:

    myDrive = drive.DifferentialDrive
    kP = tunable(0.1)
    gyro = ADXRS450_Gyro
    leftEncoder = Encoder
    rightEncoder = Encoder

    def __init__(self):
        self.powerLeft = 0
        self.powerRight = 0
        self.power = 0
        self.STICK_DEADBAND = 0.005
        self.CENTER = 0.0
        self.option = 0
        self.angle = 0
        self.distance = 0
        self.initial_run = False

    def stickDeadband(self, value):
        if value < (self.CENTER + self.STICK_DEADBAND) and value > (self.CENTER - self.STICK_DEADBAND):
            return self.CENTER
        return value

    def moveAngle(self, power, angle):
        self.power = -power
        self.angle = self.kP * (self.gyro.getAngle() - angle)
        self.option = 1

    def moveAuto(self, power, angle):
        self.power = -power
        self.angle = angle
        self.option = 1

    def moveDistance(self, power, angle, distance):
        self.power = -power
        self.angle = angle
        self.distance = distance
        self.option = 2

    def moveTank(self, powerLeft, powerRight):
        self.powerLeft = self.stickDeadband(powerLeft)
        self.powerRight = self.stickDeadband(powerRight)
        self.option = 3

    def execute(self):
        if self.option == 3:
            self.myDrive.tankDrive(self.powerLeft, self.powerRight)
        elif self.option == 2:
            while self.leftEncoder.getDistance() < self.distance:
                self.myDrive.arcadeDrive(self.power, self.angle)
        else:
            self.myDrive.arcadeDrive(self.power, self.angle)
        self.power = 0
        self.angle = 0
