from magicbot import AutonomousStateMachine, state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder
import pathfinder as pf
from pathfinder.followers import EncoderFollower
import math
import RobotMap

class PathFinder(AutonomousStateMachine):

    MODE_NAME = "Path Finder"
    DEFAULT = False

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro
    leftEncoder = Encoder
    rightEncoder = Encoder

    def on_enable(self):
        super().on_enable()
        points = [
            pf.Waypoint(0, 0, 0),
            pf.Waypoint(-5, 0, 0)
        ]

        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC,
                                       pf.SAMPLES_HIGH, RobotMap.dt, RobotMap.max_velocity, RobotMap.max_acceleration, RobotMap.max_jerk)

        # Wheelbase Width = 0.5m
        modifier = pf.modifiers.TankModifier(trajectory).modify(RobotMap.Width_Base)
        # Do something with th Te new Trajectories...
        leftTrajectory = modifier.getLeftTrajectory()
        rightTrajectory = modifier.getRightTrajectory()

        print(leftTrajectory)
        print(rightTrajectory)

        self.left = EncoderFollower(leftTrajectory)
        self.right = EncoderFollower(rightTrajectory)

        self.left.configureEncoder(self.leftEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
        self.right.configureEncoder(self.rightEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
        self.left.configurePIDVA(RobotMap.kp, RobotMap.ki, RobotMap.kd, RobotMap.kv, RobotMap.ka)
        self.right.configurePIDVA(RobotMap.kp, RobotMap.ki, RobotMap.kd, RobotMap.kv, RobotMap.ka)

        self.left.reset()
        self.right.reset()

    @state(first=True)
    def pathFinder(self, initial_call):
        powerLeft = self.left.calculate(-self.leftEncoder.get())
        powerRight = self.right.calculate(-self.rightEncoder.get())
        print(powerLeft, powerRight)
        self.driveTrain.movePathFinder(powerLeft, powerRight)
