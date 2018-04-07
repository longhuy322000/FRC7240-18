from magicbot import AutonomousStateMachine, state, timed_state
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber
from components.DriveTrain import DriveTrain
from wpilib import DriverStation, ADXRS450_Gyro
from robotpy_ext.common_drivers import navx
from networktables.networktable import NetworkTable

from robotpy_ext.misc.looptimer import LoopTimer

class MiddlePathFinder(AutonomousStateMachine):

    MODE_NAME = "Middle Pathfinder"
    DEFAULT = True

    table = NetworkTable

    pathFinder = PathFinder
    operateArm = OperateArm
    operateGrabber = OperateGrabber
    gyro = navx.AHRS
    driveTrain = DriveTrain

    def __init__(self):
        self.gameData = None
        self.supportLeftAlliance = False
        self.supportMiddleAlliance = False
        self.supportRightAlliance = False

    @timed_state(duration=0.2, first=True, next_state='goToSwitch')
    def startAutonomous(self, initial_call):
        self.operateGrabber.setGrabber('close')
        self.operateArm.setArm('up')
        self.gameData = DriverStation.getInstance().getGameSpecificMessage()
        self.supportLeftAlliance = self.table.getBoolean('supportAlliance', False)

    @state
    def goToSwitch(self, initial_call, tm):
        if initial_call:
            self.looptimer = LoopTimer(self.logger)

            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleToLeftSwitch', False, tm)
            else:
                self.pathFinder.setTrajectory('MiddleToRightSwitch', False, tm)
        self.looptimer.measure()
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitch')

    @timed_state(duration=0.3, next_state='dropCubeToSwitch')
    def lowerArmToSwitch(self):
        self.operateArm.setArm('down')

    @timed_state(duration=0.3, next_state='liftArmOutSwitch')
    def dropCubeToSwitch(self):
        self.operateGrabber.setGrabber('open')

    @timed_state(duration=0.3, next_state='backToCube')
    def liftArmOutSwitch(self):
        self.operateArm.setArm('up')

    @state
    def backToCube(self, initial_call, tm):
        if initial_call:
            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleBackLeftCube', True, tm)
            else:
                self.pathFinder.setTrajectory('MiddleBackRightCube', True, tm)
        if not self.pathFinder.running:
            self.operateArm.setArm('down')
            self.next_state('grabExtraCube')

    @state
    def grabExtraCube(self, initial_call, tm):
        if initial_call:
            self.pathFinder.setTrajectory('MiddleTakeCube', False, tm)
        if not self.pathFinder.running:
            self.next_state('grabAddCube')

    @timed_state(duration=0.3, next_state='backward')
    def grabAddCube(self):
        self.operateGrabber.setGrabber('close')

    @state
    def backward(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('MiddleBackToSwitch', True)
        if not self.pathFinder.running:
            self.next_state('liftCube')

    @timed_state(duration=0.3, next_state='goToSwitchAgain')
    def liftCube(self):
        self.operateArm.setArm('up')

    @state
    def goToSwitchAgain(self, initial_call):
        if initial_call:
            if self.gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleToLeftSwitchAgain', False)
            else:
                self.pathFinder.setTrajectory('MiddleToRightSwitchAgain', False)
        if not self.pathFinder.running:
            self.next_state('lowerArmToSwitchAgain')

    @timed_state(duration=0.3, next_state='dropCubeToSwitchAgain')
    def lowerArmToSwitchAgain(self):
        self.operateArm.setArm('down')

    @timed_state(duration=0.3, next_state='liftArmOutSwitchAgain')
    def dropCubeToSwitchAgain(self):
        self.operateGrabber.setGrabber('open')

    @timed_state(duration=0.3)
    def liftArmOutSwitchAgain(self):
        self.operateArm.setArm('up')
