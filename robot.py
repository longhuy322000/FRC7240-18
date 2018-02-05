import wpilib
from wpilib import Spark, Joystick, DoubleSolenoid, Compressor, RobotDrive, SpeedControllerGroup
from magicbot import MagicRobot
from components.DriveTrain import DriveTrain
from components.OperateCompressor import OperateCompressor
from components.OperateGrabber import OperateGrabber

class MyRobot(MagicRobot):

    driveTrain = DriveTrain
    operateGrabber = OperateGrabber
    operateCompressor = OperateCompressor

    def createObjects(self):
        self.leftFront = Spark(0)
        self.leftBack = Spark(1)
        self.rightFront = Spark(2)
        self.rightBack = Spark(3)

        self.rightFront.setInverted(True)
        self.rightBack.setInverted(True)
        self.leftFront.setInverted(True)
        self.leftBack.setInverted(True)

        self.myDrive = RobotDrive(self.leftFront, self.leftBack, self.rightFront, self.rightBack)

        self.compressor = Compressor()
        self.grabber = DoubleSolenoid(0, 1)

        self.gamepad = Joystick(0)

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.driveTrain.move(self.gamepad.getRawAxis(1), self.gamepad.getRawAxis(5))

        if self.gamepad.getRawButton(1):
            self.operateGrabber.setGrabber(True, False)
        if self.gamepad.getRawButton(2):
            self.operateGrabber.setGrabber(False, True)

        if self.gamepad.getRawButton(5):
            self.operateCompressor.setCompressor(True)
        if self.gamepad.getRawButton(6):
            self.operateCompressor.setCompressor(False)

if __name__ == '__main__':
    wpilib.run(MyRobot)
