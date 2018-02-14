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
    def moveForward(self, initial_call):
        if self.leftEncoder.getDistance() < 12:
                self.driveTrain.moveAuto(1, 0)
        else:
            self.driveTrain.moveAuto(0, 0)
            self.next_state('moveBackward')

    @state
    def moveBackward(self):
        if abs(self.leftEncoder.getDistance()) < 6:
            self.driveTrain.moveAuto(-1, 0)
        else:
            self.next_state('stopMotor')

    @state
    def stopMotor(self):
        self.driveTrain.stopMotor()
