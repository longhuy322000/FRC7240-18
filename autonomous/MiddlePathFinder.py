from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from components.DriveTrain import DriveTrain
from wpilib import DriverStation, ADXRS450_Gyro
from networktables.networktable import NetworkTable

class MiddlePathFinder(AutonomousStateMachine):

    MODE_NAME = "Middle Pathfinder"
    DEFAULT = True

    table = NetworkTable

    pathFinder = PathFinder
    operateArm = OperateArm
    operateGrabber = OperateGrabber
    gyro = ADXRS450_Gyro
    driveTrain = DriveTrain

    def __init__(self):
        self.gameData = None
        self.supportLeftAlliance = False
        self.supportMiddleAlliance = False
        self.supportRightAlliance = False

    @timed_state(duration=0.2, first=True, next_state='goToSwitch')
    def openGrabber(self, initial_call):
        self.operateGrabber.setGrabber(True)
        self.gameData = DriverStation.getInstance().getGameSpecificMessage()
        self.supportLeftAlliance = self.table.getBoolean('supportLeftAlliance', False)
        self.supportMiddleAlliance = self.table.getBoolean('supportMiddleAlliance', False)
        self.supportRightAlliance = self.table.getBoolean('supportRightAlliance', False)

    @state
    def goToSwitch(self, initial_call):
        if initial_call:
            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleToLeftSwitch', False)
            else:
                self.pathFinder.setTrajectory('MiddleToRightSwitch', False)
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitch')

    @timed_state(duration=0.5, next_state='dropCubeToSwitch')
    def lowerArmToSwitch(self):
        self.operateArm.setArm(False)

    @timed_state(duration=1, next_state='liftArmOutSwitch')
    def dropCubeToSwitch(self):
        self.operateGrabber.setGrabber(False)

    @timed_state(duration=0.4, next_state='backToCube')
    def liftArmOutSwitch(self):
        self.operateArm.setArm(True)

    @state
    def backToCube(self, initial_call):
        if initial_call:
            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleBackLeftCube', True)
            else:
                self.pathFinder.setTrajectory('MiddleBackRightCube', True)
        if not self.pathFinder.running:
            self.operateArm.setArm(False)
            self.next_state('lowerArm')

    @timed_state(duration=0.4)
    def lowerArm(self):
        self.operateArm.setArm(False)

    '''@state
    def grabExtraCube(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('MiddleTakeCube', False)
        if not self.pathFinder.running:
            self.next_state('grabAddCube')

    @timed_state(duration=0.5, next_state='rotate180')
    def grabAddCube(self):
        self.operateGrabber.setGrabber(True)

    @timed_state(duration=1, next_state='exchangeCube')
    def rotate180(self, initial_call):
        if initial_call:
            self.gyro.reset()
        self.driveTrain.moveAngle(0.5, 180)

    @state
    def exchangeCube(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('MiddleBackToPortal', False)
        if not self.pathFinder.running:
            pass'''
