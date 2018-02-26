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

    @timed_state(duration=0.2, first=True, next_state='closeGrabber')
    def openGrabber(self):
        supportAlliance = table.getBoolean('SupportAlliance', 0)
        print(supportAlliance )
        self.operateGrabber.setGrabber(False)
        self.operateArm.setArm(False)

    @timed_state(duration=0.2, next_state='goToSwitch')
    def closeGrabber(self):
        self.operateGrabber.setGrabber(True)

    @state
    def goToSwitch(self, initial_call):
        if initial_call:
            gameData = DriverStation.getInstance().getGameSpecificMessage()
            if gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleToLeftSwitch', False)
            else:
                self.pathFinder.setTrajectory('MiddleToRightSwitch', False)
        if not self.pathFinder.running:
            self.next_state('backToCube')

    @state
    def backToCube(self, initial_call):
        if initial_call:
            gameData = DriverStation.getInstance().getGameSpecificMessage()
            if gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleBackLeftSwitch', True)
            else:
                self.pathFinder.setTrajectory('MiddleBackRightSwitch', True)
        if not self.pathFinder.running:
            self.next_state('grabExtraCube')

    @state
    def grabExtraCube(self, initial_call):
        if initial_call:
            gameData = DriverStation.getInstance().getGameSpecificMessage()
            if gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleExtraLeftCube', False)
            else:
                self.pathFinder.setTrajectory('MiddleExtraRightCube', False)
