import wpilib
from wpilib import Spark, Joystick, DoubleSolenoid, Compressor, drive, SpeedControllerGroup
import magicbot
from components import DriveTrain, OperateGrabber, OperateCompressor

class MyRobot(magicbot.MagicRobot):

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

        self.m_left = SpeedControllerGroup(self.leftFront, self.leftBack)
        self.m_right = SpeedControllerGroup(self.rightFront, self.rightBack)
        self.myDrive = drive.DifferentialDrive(self.m_left, self.m_right)

        self.compressor = Compressor()
        self.grabber = DoubleSolenoid(0, 1)

        self.gamepad = Joystick(0)

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.driveTrain.move(self.gamepad.getRawAxis(1), self.gamepad.getRawAxis(5))

        if self.gamepad.getRawAxis(1):
            self.operateGrabber.setGrabber(True, False)
        if self.gamepad.getRawAxis(2):
            self.operateGrabber.setGrabber(False, True)

        if self.gamepad.getRawAxis(5):
            self.operateCompressor.setCompressor(True)
        if self.gamepad.getRawAxis(6):
            self.operateCompressor.setCompressor(False)

if __name__ == '__main__':
    wpilib.run(MyRobot)
