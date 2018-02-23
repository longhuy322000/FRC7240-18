from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from wpilib import DriverStation

class MiddlePathFinder(AutonomousStateMachine):

    MODE_NAME = "Middle Pathfinder"
    DEFAULT = False

    pathFinder = PathFinder
    operateArm = OperateArm
    operateGrabber = OperateGrabber

    @timed_state(duration=0.5, first=True, next_state='lowerArm')
    def openGrabber(self):
        self.operateGrabber.setGrabber(False)

    @timed_state(duration=0.5, next_state='closeGrabber')
    def lowerArm(self):
        self.operateArm.setArm(False)

    @timed_state(duration=0.5, next_state='liftArm')
    def closeGrabber(self):
        self.operateGrabber.setGrabber(True)

    @timed_state(duration=0.5, next_state='middleLocation')
    def liftArm(self):
        self.operateArm.setArm(True)

    @state()
    def middleLocation(self, initial_call):
        if initial_call:
            gameData = DriverStation.getInstance().getGameSpecificMessage()
            if gameData[0] == 'R':
                self.pathFinder.setTrajectory('MiddleRight', False)
            else:
                self.pathFinder.setTrajectory('MiddleLeft', False)
