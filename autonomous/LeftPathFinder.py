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
        self.gameData = DriverStation.getInstance().getGameSpecificMessage()
        self.supportLeftAlliance = self.table.getBoolean('supportLeftAlliance', False)
        self.supportMiddleAlliance = self.table.getBoolean('supportMiddleAlliance', False)
        self.supportRightAlliance = self.table.getBoolean('supportRightAlliance', False)
        self.operateGrabber.setGrabber(True)
        '''if self.gameData[0] == 'R':
            self.next_state('forward')
        else:
            self.next_state('goToSwitch')

    @timed_state(duration=5)
    def forward(self):
        self.driveTrain.moveAuto(0.5, 0)

    @state
    def goToSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('LeftSwitchLeft', False)
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitch')

    @timed_state(duration=0.3, next_state='dropCube')
    def lowerArmToSwitch(self):
        self.operateArm.setArm(False)

    @timed_state(duration=0.3, next_state='liftArmOutSwitch')
    def dropCube(self):
        self.operateGrabber.setGrabber(False)

    @timed_state(duration=0.2, next_state='readyForScale')
    def liftArmOutSwitch(self):
        self.operateArm.setArm(True)

    @state
    def readyForScale(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('LeftSwitchBack', True)
        if not self.pathFinder.running:
            self.next_state('takeCubeLeftSwitch')

    @state
    def takeCubeLeftSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('TakeCubeLeftSwitch', False)

    @state
    def supportSwitchAlliance1(self, initial_call):
        if initial_call:
            self.operateArm.setArm(False)
            self.operateGrabber.setGrabber(False)
            self.pathFinder.setTrajectory('LeftSwitchRight1', False)
        if not self.pathFinder.running:
            self.next_state('supportSwitchAlliance2')

    @state
    def supportSwitchAlliance2(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('LeftSwitchRight2', False)
        if not self.pathFinder.running:
            self.next_state('supportLiftArm')

    @timed_state(duration=0.5, next_state='supportLiftArm')
    def supportcloseGrabber(self):
        self.operateGrabber.setGrabber(True)

    @timed_state(duration=0.3, next_state='driveToSwitch')
    def supportLiftArm(self):
        self.operateArm.setArm(True)

    @timed_state(duration=0.3, next_state='supportLowerArm')
    def driveToSwitch(self):
        self.driveTrain.moveAuto(1, 0)

    @timed_state(duration=0.5, next_state='supportDropCube')
    def supportLowerArm(self):
        self.operateArm.setArm(False)

    @timed_state(duration=0.3)
    def supportDropCube(self):
        self.operateGrabber.setGrabber(False)

    @state
    def crossAutoLine(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('LeftGoForward', False)'''
