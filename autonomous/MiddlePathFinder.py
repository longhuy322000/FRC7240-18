#xPosition: 3.75, yPosition: 14

from magicbot import AutonomousStateMachine, state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder, DriverStation
import pathfinder as pf
from pathfinder.followers import EncoderFollower
import RobotMap

class PathFinder(AutonomousStateMachine):

    MODE_NAME = "Middle Pathfinder"
    DEFAULT = True

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro
    leftEncoder = Encoder
    rightEncoder = Encoder

    def on_enable(self):
        super().on_enable()

        gameData = DriverStation.getInstance().getGameSpecificMessage()
        if gameData[0] == 'R':
            points = [
                pf.Waypoint(0, 0, pf.d2r(0)),
                pf.Waypoint(7, -8.5, pf.d2r(0)),
                pf.Waypoint(10.5, -7, pf.d2r(90)),
                #pf.Waypoint(8.5, -7, pf.d2r(60))
            ]
        else:
            points = [
                pf.Waypoint(0, 0, pf.d2r(0)),
                pf.Waypoint(7, 8.5, pf.d2r(0)),
                pf.Waypoint(10.5, 7, pf.d2r(90)),
                #pf.Waypoint(8.5, -7, pf.d2r(60))
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

        RobotMap.angle_error = 0.0

        self.left.reset()
        self.right.reset()

    @state(first=True)
    def pathFinder(self, initial_call):
        powerLeft = self.left.calculate(self.leftEncoder.get())
        powerRight = self.right.calculate(self.rightEncoder.get())

        gyro_heading = -self.gyro.getAngle()
        desired_heading = pf.r2d(self.left.getHeading())
        angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
        #turn = 0.8 * (-1.0/80.0) * angleDifference
        turn = turn = RobotMap.gp * angleDifference + (RobotMap.gd *
                ((angleDifference - RobotMap.angle_error) / RobotMap.dt));
        print(desired_heading , gyro_heading, angleDifference, turn)

        RobotMap.angle_error = angleDifference

        #print(powerLeft, powerRight)
        self.driveTrain.movePathFinder(-powerLeft+turn, -powerRight-turn)
        #self.driveTrain.movePathFinder(-powerLeft, -powerRight)
