from magicbot import AutonomousStateMachine, timed_state
from components.AutoDrive import AutoDrive
from wpilib import ADXRS450_Gyro

class DriveForward(AutonomousStateMachine):

    MODE_NAME = "Drive Forward"
    DEFAULT = True

    autoDrive = AutoDrive
    gyro = ADXRS450_Gyro

    @timed_state(duration=3, first=True)
    def moveForward(self):
        self.autoDrive.move(0.5, self.gyro.getAngle())
