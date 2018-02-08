from magicbot import AutonomousStateMachine, timed_state
from wpilib import drive

class LeftLocation(AutonomousStateMachine):

    MODE_NAME = "LeftLocation"
    DEFAULT = False

    myDrive = drive.DifferentialDrive

    def initialize(self):
        pass
        
    @timed_state(duration=1.5, first=True)
    def moveForward(self):
        self.myDrive.moveAuto(0.5, 0.5)
