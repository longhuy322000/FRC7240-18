import wpilib
from wpilib import Spark, Joystick, DoubleSolenoid, Compressor, RobotDrive, SpeedControllerGroup, drive
from magicbot import MagicRobot
from components.DriveTrain import DriveTrain
from components.OperateCompressor import OperateCompressor
from components.OperateGrabber import OperateGrabber

#Gamepad axis ports
AXIS_LEFT_X = 1;
AXIS_LEFT_Y = 2;
AXIS_SHOULDER = 3;
AXIS_RIGHT_X = 4;
AXIS_RIGHT_Y = 5;
AXIS_DPAD = 6;

#Gamepad buttons
BUTTON_A = 2;
BUTTON_B = 3;
BUTTON_X = 1;
BUTTON_Y = 4;
BUTTON_SHOULDER_LEFT = 5;
BUTTON_SHOULDER_RIGHT = 6;
BUTTON_TRIGGER_LEFT = 7;
BUTTON_TRIGGER_RIGHT = 8;
BUTTON_BACK = 9;
BUTTON_START = 10;
BUTTON_LEFT_STICK = 11;
BUTTON_RIGHT_STICK = 12;
BUTTON_MODE = -1;
BUTTON_LOGITECH = -1;

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

        self.rightFront.setInverted(True)
        self.rightBack.setInverted(True)
        self.leftFront.setInverted(True)
        self.leftBack.setInverted(True)

        self.gamepad = Joystick(0)

        self.myDrive = RobotDrive(self.leftFront, self.leftBack, self.rightFront, self.rightBack)

        self.m_left = SpeedControllerGroup(self.leftFront, self.leftBack)
        self.m_right = SpeedControllerGroup(self.rightFront, self.rightBack)
        self.myDrive = drive.DifferentialDrive(self.m_left, self.m_right)

        self.compressor = Compressor()
        self.grabber = DoubleSolenoid(0, 1)

        self.gamepad = Joystick(0)

        wpilib.CameraServer.launch('vision.py:main')
>>>>>>> cd7d560d2876da1f139adc0395061589e874d289

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.driveTrain.move(self.gamepad.getRawAxis(AXIS_LEFT_Y), self.gamepad.getRawAxis(AXIS_RIGHT_Y))

        if self.gamepad.getRawButton(BUTTON_A):
            self.operateGrabber.setGrabber(True, False)
        if self.gamepad.getRawButton(BUTTON_B):
            self.operateGrabber.setGrabber(False, True)

        if self.gamepad.getRawButton(BUTTON_SHOULDER_LEFT):
            self.operateCompressor.setCompressor(True)
        if self.gamepad.getRawButton(BUTTON_SHOULDER_RIGHT):
            self.operateCompressor.setCompressor(False)

if __name__ == '__main__':
    wpilib.run(MyRobot)
