from magicbot import AutonomousStateMachine, timed_state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder, Compressor

class DriveForward(AutonomousStateMachine):

    MODE_NAME = "Drive Forward"
    DEFAULT = False

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro
    leftEncoder = Encoder
    rightEncoder = Encoder

    compressor = Compressor

    @timed_state(duration=2.75, first=True)
    def moveForward(self, initial_call):
        if initial_call:
            self.angle = self.gyro.getAngle()
        self.driveTrain.moveAuto(1, 0)
