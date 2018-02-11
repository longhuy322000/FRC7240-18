from magicbot import AutonomousStateMachine, timed_state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro

class RightLocation(AutonomousStateMachine):

    MODE_NAME = "Right Location"
    DEFAULT = False

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro

    @timed_state(duration=1.5, first=True)
    def turnRight(self):
        self.driveTrain.moveAuto(0, 0.5)
