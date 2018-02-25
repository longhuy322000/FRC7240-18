from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from wpilib import DriverStation

class RightPathFinder(AutonomousStateMachine):

    MODE_NAME = "Right Pathfinder"
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

    @timed_state(duration=0.5, next_state='goToSwitch')
    def liftArm(self):
        self.operateArm.setArm(True)

    @state
    def goToSwitch(self, initial_call):
        gameData = DriverStation.getInstance().getGameSpecificMessage()
        if initial_call:
            if gameData[0] == 'R':
                self.pathFinder.setTrajectory('RightSwitchRight', False)
            else:
                self.pathFinder.setTrajectory('RightSwitchLeft1', False)
        if not self.pathFinder.running:
            if gameData[0] == 'R':
                    self.next_state('lowerArmToSwitch')
            else:
                self.next_state('RightSwitchState2')

    @state
    def RightSwitchState2(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightSwitchLeft2', False)
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitch')

    @timed_state(duration=0.3, next_state='readyForScale')
    def lowerArmToSwitch(self):
        self.operateArm.setArm(False)
        self.operateGrabber.setGrabber(False)

    @state
    def readyForScale(self, initial_call):
        gameData = DriverStation.getInstance().getGameSpecificMessage()
        if gameData[0] == 'R':
            if initial_call:
                self.pathFinder.setTrajectory('RightSwitchBack', True)
            if not self.pathFinder.running:
                self.next_state('takeCubeRightSwitch')

    @state
    def takeCubeRightSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('TakeCubeRightSwitch', False)
