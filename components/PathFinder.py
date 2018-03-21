from magicbot import tunable
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder, RobotBase
import pathfinder as pf
from pathfinder.followers import EncoderFollower
import RobotMap, pickle, os.path
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber


'''

'MiddleBackToPortal': [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(5, -2.5, pf.d2r(0))
],

'LeftSwitchRight1': [
    pf.Waypoint(3, 21, pf.d2r(0)),
    pf.Waypoint(10, 24, pf.d2r(0)),
    pf.Waypoint(17, 24, pf.d2r(0)),
    pf.Waypoint(22, 20, pf.d2r(-90))
],
'LeftSwitchRight2': [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(4, 0, pf.d2r(0)),
    pf.Waypoint(9, 0, pf.d2r(0)),
    pf.Waypoint(10.4, -2.2, pf.d2r(-90))
],
'LeftSwitchBack': [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(2.5, -2.5, pf.d2r(-90)),
    pf.Waypoint(-0.5, -7, pf.d2r(-90))
],
'TakeCubeLeftSwitch': [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(3.3, 2.3, pf.d2r(0))
],
],
'RightSwitchBack': [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(2.5, 2.5, pf.d2r(-90)),
    pf.Waypoint(-0.5, 7, pf.d2r(-90))
],
'TakeCubeRightSwitch': [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(3.1, -2.3, pf.d2r(0))
],
'RightSwitchLeft1': [
    pf.Waypoint(3, 21, pf.d2r(0)),
    pf.Waypoint(10, 18, pf.d2r(0)),
    pf.Waypoint(17, 18, pf.d2r(0)),
    pf.Waypoint(22, 22, pf.d2r(90))
],
'RightSwitchLeft2': [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(4, 0, pf.d2r(0)),
    pf.Waypoint(9, 0, pf.d2r(0)),
    pf.Waypoint(10.3, 2.2, pf.d2r(90))
],
'''
points = {

    'LeftSwitchLeft': [
        pf.Waypoint(1.5, 21, pf.d2r(0)),
        pf.Waypoint(10, 24, pf.d2r(0)),
        pf.Waypoint(13.5, 20, pf.d2r(-90))
    ],

    'LeftGoForward': [
         pf.Waypoint(1.5, 21, pf.d2r(0)),
         pf.Waypoint(14, 24, pf.d2r(0))
     ],

    'RightGoForward': [
         pf.Waypoint(1.5, 6, pf.d2r(0)),
         pf.Waypoint(14, 3, pf.d2r(0)),
     ],

    'RightSwitchRight': [
        pf.Waypoint(1.5, 6, pf.d2r(0)),
        pf.Waypoint(10, 3, pf.d2r(0)),
        pf.Waypoint(14, 6.5, pf.d2r(90))
    ],

    'MiddleToLeftSwitch': [
        pf.Waypoint(1.5, 13, pf.d2r(0)),
        pf.Waypoint(10, 18, pf.d2r(0))
    ],

    'MiddleToRightSwitch': [
        pf.Waypoint(1.5, 13, pf.d2r(0)),
        pf.Waypoint(10, 9, pf.d2r(0))
    ],

    'MiddleBackLeftCube': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(6, 5, pf.d2r(0))
    ],

    'MiddleBackRightCube': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(6, -3.85, pf.d2r(0))
    ],

    'MiddleTakeCube': [
        pf.Waypoint(4, 13, pf.d2r(0)),
        pf.Waypoint(7, 13, pf.d2r(0))
    ],
}

pickle_file = os.path.join(os.path.dirname(__file__), 'trajectory.pickle')

if RobotBase.isSimulation():
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

    active = tunable(0)

    def __init__(self):
        self.angle_error = 0.0
        self.running = True
        self.reverse = False
        self.location = None

    def setTrajectory(self, location, reverse, tm=0.0):
        self.reverse = reverse
        self.running = True
        self.angle_error = 0.0
        self.location = location

        modifier = pf.modifiers.TankModifier(points[location]).modify(RobotMap.Width_Base)

        leftTrajectory = modifier.getLeftTrajectory()
        rightTrajectory = modifier.getRightTrajectory()

        self.left = EncoderFollower(leftTrajectory)
        self.right = EncoderFollower(rightTrajectory)

        self.left.reset()
        self.right.reset()
        self.gyro.reset()

        if self.reverse:
            self.left.configureEncoder(-self.rightEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
            self.right.configureEncoder(-self.leftEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
        else:
            self.left.configureEncoder(self.leftEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
            self.right.configureEncoder(self.rightEncoder.get(), 360, RobotMap.WHEEL_DIAMETER)
        self.left.configurePIDVA(self.kp, self.ki, self.kd, self.kv, self.ka)
        self.right.configurePIDVA(self.kp, self.ki, self.kd, self.kv, self.ka)

        if RobotBase.isSimulation():
            from pyfrc.sim import get_user_renderer
            renderer = get_user_renderer()
            if renderer:
                if self.reverse:
                    renderer.draw_pathfinder_trajectory(leftTrajectory, color='#0000ff', offset=(1,0), scale=(-1,-1))
                    renderer.draw_pathfinder_trajectory(modifier.source, color='#00ff00', scale=(-1,-1), show_dt=1.0, dt_offset=tm)
                    renderer.draw_pathfinder_trajectory(rightTrajectory, color='#0000ff', offset=(-1,0), scale=(-1,-1))
                else:
                    renderer.draw_pathfinder_trajectory(leftTrajectory, color='#0000ff', offset=(-1,0))
                    renderer.draw_pathfinder_trajectory(modifier.source, color='#00ff00', show_dt=1.0, dt_offset=tm)
                    renderer.draw_pathfinder_trajectory(rightTrajectory, color='#0000ff', offset=(1,0))

    def execute(self):
        if not self.running:
            return

        if self.reverse:
            powerLeft = self.left.calculate(-self.rightEncoder.get())
            powerRight = self.right.calculate(-self.leftEncoder.get())
            current_gp = -self.gp
        else:
            powerLeft = self.left.calculate(self.leftEncoder.get())
            powerRight = self.right.calculate(self.rightEncoder.get())
            current_gp = self.gp

        gyro_heading = -self.gyro.getAngle()
        desired_heading = pf.r2d(self.left.getHeading())
        angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
        turn = current_gp * angleDifference + (self.gd *
                ((angleDifference - self.angle_error) / self.dt))
        self.angle_error = angleDifference

        if self.reverse:
            self.driveTrain.movePathFinder(powerRight, powerLeft)
        else:
            self.driveTrain.movePathFinder(-powerLeft+turn, -powerRight-turn)

        if self.left.isFinished() or self.right.isFinished():
            if abs(pf.boundHalfDegrees(angleDifference)) > 5:
                if self.location == 'MiddleExtraRightCube':
                    self.driveTrain.moveAngle(0.5, pf.boundHalfDegrees(desired_heading))
                else:
                    self.driveTrain.moveAngle(0.5, pf.boundHalfDegrees(-desired_heading))
            else:
                self.running = False
            #print(desired_heading, gyro_heading, turn, angleDifference)

    def on_disable(self):
        self.running = False
