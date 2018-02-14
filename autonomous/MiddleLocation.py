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

    action = {'1': False, '2': False}

    @state(first=True)
    def moveForward(self, initial_call):
        if not self.action['1']:
            if self.leftEncoder.getDistance() < 12:
                self.driveTrain.moveAuto(1, 0)
            else:
                self.action['1'] = True
                self.driveTrain.moveAuto(0, 0)
        elif not self.action['2']:
            #print(self.leftEncoder.getDistance())
            if abs(self.leftEncoder.getDistance()) < 6:
                self.driveTrain.moveAuto(-1, 0)
            else:
                self.action['2'] = True
                self.leftEncoder.reset()
                self.rightEncoder.reset()
