from magicbot import AutonomousStateMachine, timed_state
from components.AutoDrive import AutoDrive
from wpilib import ADXRS450_Gyro

class MiddleLocation(AutonomousStateMachine):

    MODE_NAME = "Middle Location"
    DEFAULT = False

    autoDrive = AutoDrive
    gyro = ADXRS450_Gyro

    @timed_state(duration=1.5, first=True, next_state='turnRight')
    def turnLeft(self):
        self.autoDrive.move(0, -0.5)

    @timed_state(duration=1.5)
    def turnRight(self):
        self.autoDrive.move(0, 0.5)
