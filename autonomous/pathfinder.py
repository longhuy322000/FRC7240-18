from magicbot import AutonomousStateMachine, state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder
import pathfinder as pf
from pathfinder.followers import EncoderFollower
import math

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
            pf.Waypoint(1, 4, 0),
            pf.Waypoint(2, 2, 0)
        ]

        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC,
                                       pf.SAMPLES_HIGH, 0.02, 1.7, 2.0, 60.0)

        # Wheelbase Width = 0.5m
        modifier = pf.modifiers.TankModifier(trajectory).modify(2)

        # Do something with th Te new Trajectories...
        leftTrajectory = modifier.getLeftTrajectory()
        rightTrajectory = modifier.getRightTrajectory()

        self.left = EncoderFollower(leftTrajectory)
        self.right = EncoderFollower(rightTrajectory)

        self.left.configureEncoder(self.leftEncoder.get(), 360, 0.5)
        self.right.configureEncoder(self.rightEncoder.get(), 360, 0.5)
        self.left.configurePIDVA(0.8, 0.0, 0.0, 0.25, 0.0)
        self.right.configurePIDVA(0.8, 0.0, 0.0, 0.25, 0.0)

        self.left.reset()
        self.right.reset()

    @state(first=True)
    def pathFinder(self, initial_call):
        powerLeft = self.left.calculate(self.leftEncoder.get())
        powerRight = self.right.calculate(self.rightEncoder.get())
        self.driveTrain.movePathFinder(powerLeft, powerRight)
