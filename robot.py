#!/usr/bin/env python3

import wpilib
from wpilib import Spark, Joystick, DoubleSolenoid, Compressor, SpeedControllerGroup, drive, CameraServer, ADXRS450_Gyro, Encoder
from magicbot import MagicRobot
from components.DriveTrain import DriveTrain
from components.OperateCompressor import OperateCompressor
from components.OperateGrabber import OperateGrabber
from components.PathFinder import PathFinder
from components.OperateArm import OperateArm
import math
import RobotMap

# Gamepad Axis
leftStick_X = 0
leftStick_Y = 1
shoulderAxisLeft = 2
shoulderAxisRight = 3
rightStick_X = 4
rightStick_Y = 5
dpadAxis = 6

# Gamepad Buttons
BUTTON_A = 1
BUTTON_B = 2
BUTTON_X = 3
BUTTON_Y = 4
BUTTON_L_SHOULDER = 5
BUTTON_R_SHOULDER = 6
BUTTON_BACK = 7
BUTTON_START = 8
BUTTON_LEFTSTICK = 9
BUTTON_RIGHTSTICK = 10

if wpilib.RobotBase.isSimulation():
    rightStick_Y = 3

class MyRobot(MagicRobot):

    pathFinder = PathFinder
    driveTrain = DriveTrain
    operateGrabber = OperateGrabber
    operateCompressor = OperateCompressor
    operateArm = OperateArm


    def createObjects(self):
        self.leftFront = Spark(2)
        self.leftBack = Spark(3)
        self.rightFront = Spark(0)
        self.rightBack = Spark(1)
        self.rightFront.setInverted(True)
        self.rightBack.setInverted(True)
        self.leftFront.setInverted(True)
        self.leftBack.setInverted(True)

        self.m_left = SpeedControllerGroup(self.leftFront, self.leftBack)
        self.m_right = SpeedControllerGroup(self.rightFront, self.rightBack)
        self.myDrive = drive.DifferentialDrive(self.m_left, self.m_right)
        self.myDrive.setSafetyEnabled(False)

        self.compressor = Compressor()
        self.grabber = DoubleSolenoid(0, 1)
        self.armSolenoid = DoubleSolenoid(2, 3)

        self.gamepad = Joystick(0)

        self.gyro = ADXRS450_Gyro()

        self.leftEncoder = Encoder(0, 1, False, Encoder.EncodingType.k4X)
        self.rightEncoder = Encoder(2, 3, False, Encoder.EncodingType.k4X)

        self.leftEncoder.setDistancePerPulse((1/360.0)*RobotMap.WHEEL_DIAMETER*math.pi)
        self.rightEncoder.setDistancePerPulse((1/360.0)*RobotMap.WHEEL_DIAMETER*math.pi)

        CameraServer.launch('vision.py:main')

    def autonomous(self):
        self.gyro.reset()
        super().autonomous()

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        if self.isSimulation():
            self.driveTrain.moveAuto(self.gamepad.getY(), self.gamepad.getX())
        else:
            self.driveTrain.moveTank(self.gamepad.getRawAxis(leftStick_Y), self.gamepad.getRawAxis(rightStick_Y))

        if self.gamepad.getRawAxis(shoulderAxisLeft):
            self.operateGrabber.setGrabber(True)
        elif self.gamepad.getRawAxis(shoulderAxisRight):
            self.operateGrabber.setGrabber(False)

        if self.gamepad.getRawButton(BUTTON_A):
            self.operateArm.setArm(True)
        elif self.gamepad.getRawButton(BUTTON_B):
            self.operateArm.setArm(False)

        if self.gamepad.getRawButton(BUTTON_L_SHOULDER):
            self.operateCompressor.setCompressor(True)
        if self.gamepad.getRawButton(BUTTON_R_SHOULDER):
            self.operateCompressor.setCompressor(False)

if __name__ == '__main__':
    wpilib.run(MyRobot)
