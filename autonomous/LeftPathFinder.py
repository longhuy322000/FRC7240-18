from magicbot import AutonomousStateMachine, state
from components.PathFinder import PathFinder

class LeftPathFinder(AutonomousStateMachine):

    MODE_NAME = "Left Pathfinder"
    DEFAULT = False

    pathFinder = PathFinder

    @state(first=True)
    def leftLocation(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('left')
