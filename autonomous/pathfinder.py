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

    points = [
        pf.Waypoint(-4, -1, math.radians(-45.0)),
        pf.Waypoint(-2, -2, 0),
        pf.Waypoint(0, 0, 0),
    ]

    info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC,
                                   pf.SAMPLES_HIGH, 0.05, 1.7, 2.0, 60.0)

    # Wheelbase Width = 0.5m
    modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)

    # Do something with th Te new Trajectories...
    leftTrajectory = modifier.getLeftTrajectory()
    rightTrajectory = modifier.getRightTrajectory()

    left = EncoderFollower(leftTrajectory)
    right = EncoderFollower(rightTrajectory)

    @state(first=True)
    def pathFinder(self, initial_call):
        '''if initial_call:
            x = self.left[1]
            print(x.velocity)'''
        powerLeft = self.left.calculate(self.leftEncoder.getRaw())
        powerRight = self.right.calculate(self.rightEncoder.getRaw())
        print(powerLeft, powerRight)

            #print(powerLeft, powerRight)
            #ßself.driveTrain.movePathFinder(powerLeft, powerRight)
