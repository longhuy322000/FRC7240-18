from magicbot import AutonomousStateMachine, timed_state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro

class LeftLocation(AutonomousStateMachine):

    MODE_NAME = "Left Location"
    DEFAULT = False

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro

    @timed_state(duration=1.5, first=True)
    def turnLeft(self):
        self.driveTrain.moveAuto(0, -1)
