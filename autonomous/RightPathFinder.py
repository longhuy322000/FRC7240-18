from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from wpilib import DriverStation
from networktables import NetworkTables

table = NetworkTables.getTable('SmartDashboard')

class RightPathFinder(AutonomousStateMachine):

    MODE_NAME = "Right Pathfinder"
    DEFAULT = False

    pathFinder = PathFinder
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
        self.supportLeftAlliance = table.getBoolean('supportLeftAlliance', False)
        self.supportMiddleAlliance = table.getBoolean('supportMiddleAlliance', False)
        self.supportRightAlliance = table.getBoolean('supportRightAlliance', False)
        if self.gameData[0] == 'L':
            if self.supportLeftAlliance:
                self.next_state('supportSwitchAlliance1')
            else:
                self.next_state('crossAutoLine')
        else:
            self.next_state('openGrabber')

    @state
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
            pass

    @state
    def crossAutoLine(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightGoForward', False)

    @timed_state(duration=0.2, next_state='closeGrabber')
    def openGrabber(self):
        self.operateGrabber.setGrabber(False)
        self.operateArm.setArm(False)

    @timed_state(duration=0.2, next_state='liftArm')
    def closeGrabber(self):
        self.operateGrabber.setGrabber(True)

    @timed_state(duration=0.2, next_state='goToSwitch')
    def liftArm(self):
        self.operateArm.setArm(True)

    @state
    def goToSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightSwitchRight', False)
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitch')

    @timed_state(duration=0.3, next_state='readyForScale')
    def lowerArmToSwitch(self):
        self.operateArm.setArm(False)
        self.operateGrabber.setGrabber(False)

    @state
    def readyForScale(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('RightSwitchBack', True)
        if not self.pathFinder.running:
            self.next_state('takeCubeRightSwitch')

    @state
    def takeCubeRightSwitch(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('TakeCubeRightSwitch', False)
