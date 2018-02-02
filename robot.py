import wpilib
from wpilib import Spark, Joystick, RobotDrive, DoubleSolenoid
import magicbot
from components import DriveTrain

class MyRobot(magicbot.MagicRobot):

    driveTrain = DriveTrain


    def createObjects(self):
        self.leftFront = Spark(0)
        self.leftBack = Spark(1)
        self.rightFront = Spark(2)
        self.rightBack = Spark(3)

        self.grabber = DoubleSolenoid(0, 1)

        self.rightFront.setInverted(true);
		self.rightBack.setInverted(true);
		self.leftFront.setInverted(true);
		self.leftBack.setInverted(true);

        self.gamepad = Joystick(0)

        self.myDrive = RobotDrive(leftFront, leftBack, rightFront, rightBack)

    def teleopInit(self):


    def teleopPeriodic(self):
        self.driveTrain.move(self.gamepad.getRawAxis(1), self.gamepad.getRawAxis(5))

if __name__ == '__main__':
    wpilib.run(MyRobot)
