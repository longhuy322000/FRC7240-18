from magicbot import timed_state, AutonomousStateMachine
from components.DriveTrain import DriveTrain

class DriveForward(AutonomousStateMachine):

    MODE_NAME = 'Drive Forward'
    DEFAULT = True

    driveTrain = DriveTrain

    @timed_state(duration=3, first=True)
    def moveForward(self):
        self.driveTrain.moveAuto(-0.5, -0.5)
