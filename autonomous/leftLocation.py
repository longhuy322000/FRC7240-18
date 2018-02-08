from magicbot import AutonomousStateMachine, timed_state
from components.AutoDrive import AutoDrive
from wpilib import ADXRS450_Gyro

class LeftLocation(AutonomousStateMachine):

    MODE_NAME = "Left Location"
    DEFAULT = False

    autoDrive = AutoDrive
    gyro = ADXRS450_Gyro

    @timed_state(duration=1.5, first=True)
    def turnLeft(self):
        self.autoDrive.move(0, -0.5)
