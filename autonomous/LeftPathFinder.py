from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from components.DriveTrain import DriveTrain
from wpilib import DriverStation
from networktables.networktable import NetworkTable

class LeftPathFinder(AutonomousStateMachine):

    MODE_NAME = "Left Pathfinder"
    DEFAULT = False

    table = NetworkTable
    pathFinder = PathFinder
    operateArm = OperateArm
    operateGrabber = OperateGrabber
    driveTrain = DriveTrain

    def __init__(self):
        self.gameData = None
        self.supportLeftAlliance =False
        self.supportMiddleAlliance = False
        self.supportRightAlliance = False

    @state(first=True)
    def startAutonomous(self):
        self.operateGrabber.setGrabber('close')
        self.operateArm.setArm('up')
        self.gameData = DriverStation.getInstance().getGameSpecificMessage()
        self.supportLeftAlliance = self.table.getBoolean('supportAlliance', False)
        if self.gameData[0] == 'R':
            self.next_state('goForward')
        else:
            self.next_state('goToSwitch')

    @state
    def goForward(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('LeftGoForward', False)

    @state
    def goToSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('LeftSwitchLeft', False)
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitch')

    @timed_state(duration=0.1, next_state='dropCube')
    def lowerArmToSwitch(self):
        self.operateArm.setArm('down')

    @timed_state(duration=0.3, next_state='liftArmOutSwitch')
    def dropCube(self):
        self.operateGrabber.setGrabber('open')

    @timed_state(duration=0.2)
    def liftArmOutSwitch(self):
        self.operateArm.setArm('up')
