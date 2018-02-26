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

    @timed_state(duration=0.5, first=True, next_state='lowerArm')
    def openGrabber(self):
        supportAlliance = table.getBoolean('SupportAlliance', 0)
        print(supportAlliance )
        self.operateGrabber.setGrabber(False)

    @timed_state(duration=0.5, next_state='closeGrabber')
    def lowerArm(self):
        self.operateArm.setArm(False)

    @timed_state(duration=0.5, next_state='liftArm')
    def closeGrabber(self):
        self.operateGrabber.setGrabber(True)

    @timed_state(duration=0.5, next_state='prepareForPortal')
    def liftArm(self):
        self.operateArm.setArm(True)

    @state
    def prepareForPortal(self, initial_call):
        if initial_call:
            gameData = DriverStation.getInstance().getGameSpecificMessage()
            if gameData[0] == 'R':
                self.pathFinder.setTrajectory('MiddleRight', False)
            else:
                self.pathFinder.setTrajectory('PreparePortal', False)
        if not self.pathFinder.running:
            if abs(int(self.gyro.getAngle())) < 179:
                self.driveTrain.moveAngle(0.5, -180)
            else:
                self.next_state('goToPortal')

    @state
    def goToPortal(self, initial_call):
        if initial_call:
            self.pathFinder.setTrajectory('DropCubePortal', False)
        if not self.pathFinder.running:
            self.next_state('backToSwitch')

    @state
    def backToSwitch(self, initial_call):
        gameData = DriverStation.getInstance().getGameSpecificMessage()
        if initial_call:
            if gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleBackLeftSwitch', True)
            else:
                self.pathFinder.setTrajectory('MiddleBackRightSwitch', True)
        if not self.pathFinder.running:
            self.next_state('goToSwitch')

    @state
    def goToSwitch(self, initial_call):
        gameData = DriverStation.getInstance().getGameSpecificMessage()
        if initial_call:
            if gameData[0] == 'L':
                self.pathFinder.setTrajectory('MiddleToLeftSwitch', False)
            else:
                self.pathFinder.setTrajectory('MiddleToRightSwitch', False)
