#xPosition: 3.75, yPosition: 14

from magicbot import AutonomousStateMachine, state
from wpilib import DriverStation
from components.PathFinder import PathFinder

class MiddlePathFinder(AutonomousStateMachine):

    MODE_NAME = "Middle Pathfinder"
    DEFAULT = True

    pathFinder = PathFinder

    @state(first=True)
    def middleLocation(self, initial_call):
        if initial_call:
            gameData = DriverStation.getInstance().getGameSpecificMessage()
            if gameData[0] == 'R':
                self.pathFinder.setTrajectory('middleright')
            else:
                self.pathFinder.setTrajectory('middleleft')
