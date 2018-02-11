from magicbot import AutonomousStateMachine, state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder

class MiddleLocation(AutonomousStateMachine):

    MODE_NAME = "Middle Location"
    DEFAULT = False

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro
    leftEncoder = Encoder
    rightEncoder = Encoder

    @state(first=True)
    def moveForward(self):
        '''while self.leftEncoder.getDistance() < 6:
            self.driveTrain.moveAuto(1, 0)'''
        self.driveTrain.moveDistance(1, 0, 6)
