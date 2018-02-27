from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from components.DriveTrain import DriveTrain
from wpilib import DriverStation, ADXRS450_Gyro
from networktables import NetworkTables

table = NetworkTables.getTable('SmartDashboard')

class MiddlePathFinder(AutonomousStateMachine):

    MODE_NAME = "Middle Pathfinder"
    DEFAULT = True

    pathFinder = PathFinder
    operateArm = OperateArm
    operateGrabber = OperateGrabber
    gyro = ADXRS450_Gyro
    driveTrain = DriveTrain

    def __init__(self):
        self.gameData = None
        self.supportLeftAlliance =False
        self.supportMiddleAlliance = False
        self.supportRightAlliance = False

    @timed_state(duration=0.2, first=True, next_state='closeGrabber')
    def openGrabber(self):
        self.gameData = DriverStation.getInstance().getGameSpecificMessage()
        self.supportLeftAlliance = table.getBoolean('supportLeftAlliance', False)
        self.supportMiddleAlliance = table.getBoolean('supportMiddleAlliance', False)
        self.supportRightAlliance = table.getBoolean('supportRightAlliance', False)
        self.operateGrabber.setGrabber(False)
        self.operateArm.setArm(False)

    @timed_state(duration=0.2, next_state='goToSwitch')
    def closeGrabber(self):
        self.operateGrabber.setGrabber(True)

    @state
    def goToSwitch(self, initial_call):
        if initial_call:
            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleToLeftSwitch', False)
            else:
                self.pathFinder.setTrajectory('MiddleToRightSwitch', False)
        if not self.pathFinder.running:
            self.next_state('backToCube')

    @state
    def backToCube(self, initial_call):
        if initial_call:
            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleBackLeftSwitch', True)
            else:
                self.pathFinder.setTrajectory('MiddleBackRightSwitch', True)
        if not self.pathFinder.running:
            self.next_state('grabExtraCube')

    @state
    def grabExtraCube(self, initial_call):
        if initial_call:
            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleLeftCrossLine', False)
            else:
                self.pathFinder.setTrajectory('MiddleRightCrossLine', False)
