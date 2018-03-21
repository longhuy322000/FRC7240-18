from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from components.DriveTrain import DriveTrain
from wpilib import DriverStation
from networktables.networktable import NetworkTable

class RightPathFinder(AutonomousStateMachine):

    MODE_NAME = "Right Pathfinder"
    DEFAULT = False

    table = NetworkTable

    pathFinder = PathFinder
    driveTrain = DriveTrain
    operateArm = OperateArm
    operateGrabber = OperateGrabber

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
        if self.gameData[0] == 'R':
            self.next_state('goToSwitch')
        else:
            self.next_state('goForward')

    @timed_state(duration=5)
    def goForward(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightGoForward', False)

    @state
    def goToSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightSwitchRight', False)
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitch')

    @timed_state(duration=0.3, next_state='dropCube')
    def lowerArmToSwitch(self):
        self.operateArm.setArm(False)

    @timed_state(duration=0.3, next_state='liftArmOutSwitch')
    def dropCube(self):
        self.operateGrabber.setGrabber(False)

    @timed_state(duration=0.2)
    def liftArmOutSwitch(self):
        self.operateArm.setArm(True)

    '''@state
    def supportSwitchAlliance1(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightSwitchLeft1', False)
        if not self.pathFinder.running:
            self.next_state('supportSwitchAlliance2')
    @state
    def supportSwitchAlliance2(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightSwitchLeft2', False)
        if not self.pathFinder.running:
            self.next_state('supportcloseGrabber')
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
            self.pathFinder.setTrajectory('RightGoForward', False)'''

    '''@state
    def readyForScale(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightSwitchBack', True)
        if not self.pathFinder.running:
            self.next_state('takeCubeRightSwitch')
    @state
    def takeCubeRightSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('TakeCubeRightSwitch', False)'''
