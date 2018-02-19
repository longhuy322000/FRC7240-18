from magicbot import AutonomousStateMachine, state
from components.PathFinder import PathFinder

class RightPathFinder(AutonomousStateMachine):

    MODE_NAME = "Right Pathfinder"
    DEFAULT = False

    pathFinder = PathFinder

    @state(first=True)
    def rightLocation(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('right')
