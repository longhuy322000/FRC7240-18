from magicbot import tunable
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder, RobotBase
import pathfinder as pf
from pathfinder.followers import EncoderFollower
import RobotMap, pickle, wpilib
import os.path
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber

points = {
    'MiddleLeft': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(9, 9.5, pf.d2r(0)),
        pf.Waypoint(12.25, 7.65, pf.d2r(90))
    ],

    'MiddleRight': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(9, -9.5, pf.d2r(0)),
        pf.Waypoint(12.25, -7.65, pf.d2r(90))
    ],

    'Left': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(10, 3, pf.d2r(0)),
        pf.Waypoint(11.5, -0.8, pf.d2r(90))
    ],

    'Right': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(10, -3, pf.d2r(0)),
        pf.Waypoint(11.5, 0.8, pf.d2r(90))
    ]
}

pickle_file = os.path.join(os.path.dirname(__file__), 'trajectory.pickle')

if wpilib.RobotBase.isSimulation():
    for key, value in points.items():
        info, trajectory = pf.generate(value, pf.FIT_HERMITE_CUBIC,
                                       pf.SAMPLES_HIGH, RobotMap.dt, RobotMap.max_velocity, RobotMap.max_acceleration, RobotMap.max_jerk)
        points[key] = trajectory
    with open(pickle_file, 'wb') as f:
        pickle.dump(points, f, pickle.HIGHEST_PROTOCOL)

with open(pickle_file, 'rb') as f:
        points = pickle.load(f)

class PathFinder:

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro
    leftEncoder = Encoder
    rightEncoder = Encoder
    operateArm = OperateArm
    operateGrabber = OperateGrabber

    kp = tunable(RobotMap.kp)
    ki = tunable(RobotMap.ki)
    kd = tunable(RobotMap.kd)
    kv = tunable(RobotMap.kv)
    ka = tunable(RobotMap.ka)
    gp = tunable(RobotMap.gp)
    gd = tunable(RobotMap.gd)
    dt = tunable(RobotMap.dt)
    max_velocity = tunable(RobotMap.max_velocity)
    max_acceleration = tunable(RobotMap.max_acceleration)
    max_jerk = tunable(RobotMap.max_jerk)

    def __init__(self):
        self.points = []
        self.check = False
        self.angle_error = 0.0
        self.running = False

    def setTrajectory(self, location):
        if location == 'middleright':
            modifier = pf.modifiers.TankModifier(points['MiddleRight']).modify(RobotMap.Width_Base)
        elif location == 'middleleft':
            modifier = pf.modifiers.TankModifier(points['MiddleLeft']).modify(RobotMap.Width_Base)
        elif location == 'left':
            modifier = pf.modifiers.TankModifier(points['Left']).modify(RobotMap.Width_Base)
        elif location == 'right':
            modifier = pf.modifiers.TankModifier(points['Right']).modify(RobotMap.Width_Base)

        leftTrajectory = modifier.getLeftTrajectory()
        rightTrajectory = modifier.getRightTrajectory()

        self.left = EncoderFollower(leftTrajectory)
        self.right = EncoderFollower(rightTrajectory)

        self.left.configureEncoder(self.leftEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
        self.right.configureEncoder(self.rightEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
        self.left.configurePIDVA(self.kp, self.ki, self.kd, self.kv, self.ka)
        self.right.configurePIDVA(self.kp, self.ki, self.kd, self.kv, self.ka)

        self.left.reset()
        self.right.reset()
        self.gyro.reset()

        self.running = True
        
        if RobotBase.isSimulation():
            from pyfrc.sim import get_user_renderer
            renderer = get_user_renderer()
            if renderer:
                renderer.draw_pathfinder_trajectory(modifier.source)

    def execute(self):
        if not self.running:
            return

        powerLeft = self.left.calculate(self.leftEncoder.get())
        powerRight = self.right.calculate(self.rightEncoder.get())

        gyro_heading = -self.gyro.getAngle()
        desired_heading = pf.r2d(self.left.getHeading())
        angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
        #turn = 0.8 * (-1.0/80.0) * angleDifference
        turn = turn = self.gp * angleDifference + (self.gd *
                ((angleDifference - self.angle_error) / self.dt));
        self.angle_error = angleDifference

        self.driveTrain.movePathFinder(-powerLeft+turn, -powerRight-turn)
        if self.left.isFinished() or self.right.isFinished():
            self.operateArm.setArm(False)
            self.operateGrabber.setGrabber(False)
            self.running = True

    def on_disable(self):
        self.running = False
