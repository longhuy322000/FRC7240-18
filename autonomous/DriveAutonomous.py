from magicbot import AutonomousStateMachine, state
from components.DriveTrain import DriveTrain
from autonomous.RobotLocation import LeftLocation

class driveAutonomous(AutonomousStateMachine):

    MODE_NAME = "Drive Autonomous"
    DEFAULT = True

    driveTrain = DriveTrain
    #leftLocation = LeftLocation

    @state(first=True)
    def passLine(self):
        self.driveTrain.moveAuto(0.5, 0.5)
