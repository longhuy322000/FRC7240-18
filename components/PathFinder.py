import math
from magicbot import tunable
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro, Encoder, RobotBase, SmartDashboard, Timer
from robotpy_ext.common_drivers import navx
import pathfinder as pf
from pathfinder.followers import EncoderFollower
import RobotMap, pickle, os.path
from components.OperateArm import OperateArm
from components.OperateGrabber import OperateGrabber


'''

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
        pf.Waypoint(13, 20.5, pf.d2r(-90))
    ],

    'LeftGoForward': [
         pf.Waypoint(1.5, 21, pf.d2r(0)),
         pf.Waypoint(14, 24, pf.d2r(0))
     ],

    'RightSwitchRight': [
        pf.Waypoint(1.5, 6, pf.d2r(0)),
        pf.Waypoint(10, 3, pf.d2r(0)),
        pf.Waypoint(13, 6.2, pf.d2r(90))
    ],

    'RightGoForward': [
         pf.Waypoint(1.5, 6, pf.d2r(0)),
         pf.Waypoint(14, 3, pf.d2r(0)),
     ],

    'MiddleToLeftSwitch': [
        pf.Waypoint(1.5, 13, pf.d2r(0)),
        pf.Waypoint(10.5, 18.5, pf.d2r(0))
    ],

    'MiddleToRightSwitch': [
        pf.Waypoint(1.5, 13, pf.d2r(0)),
        pf.Waypoint(10.5, 8.5, pf.d2r(0))
    ],

    'MiddleBackLeftCube': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(6, 5, pf.d2r(0))
    ],

    'MiddleBackRightCube': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(6, -5, pf.d2r(0))
    ],

    'MiddleTakeCube': [
        pf.Waypoint(4, 13, pf.d2r(0)),
        pf.Waypoint(7, 13, pf.d2r(0))
    ],

    'MiddleBackToSwitch': [
        pf.Waypoint(0, 0, pf.d2r(0)),
        pf.Waypoint(3, 0, pf.d2r(0))
    ],

    'MiddleToLeftSwitchAgain': [
        pf.Waypoint(4.5, 13.5, pf.d2r(0)),
        pf.Waypoint(11.3, 18.5, pf.d2r(0))
    ],

    'MiddleToRightSwitchAgain': [
        pf.Waypoint(4.5, 13.5, pf.d2r(0)),
        pf.Waypoint(11.3, 8.5, pf.d2r(0))
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

print("Pathfinder load")

with open(pickle_file, 'rb') as f:
    points = pickle.load(f)

print("PathFinder transform")

def _loadmod(v):
    modifier = pf.modifiers.TankModifier(v).modify(RobotMap.Width_Base)

    leftTrajectory = modifier.getLeftTrajectory()
    rightTrajectory = modifier.getRightTrajectory()

    left = EncoderFollower(leftTrajectory)
    right = EncoderFollower(rightTrajectory)

    return left, right, leftTrajectory, rightTrajectory, modifier

mods = {k: _loadmod(v) for k, v in points.items()}

print("Transform done")

class PathFinder:

    driveTrain = DriveTrain
    gyro = navx.AHRS
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

    turn_limit = tunable(0.6)

    active = tunable(0)

    def __init__(self):
        self.angle_error = 0.0
        self.gyro_start = 0.0
        self.running = True
        self.reverse = False
        self.location = None

    def setTrajectory(self, location, reverse, tm=0.0):
        self.reverse = reverse
        self.running = True
        self.angle_error = 0.0
        self.location = location

        self.logger.info("setTrajectory: %s %s", location, reverse)

        self.left, self.right, leftTrajectory, rightTrajectory, modifier = mods[location]

        # modifier = pf.modifiers.TankModifier(points[location]).modify(RobotMap.Width_Base)
        #
        # leftTrajectory = modifier.getLeftTrajectory()
        # rightTrajectory = modifier.getRightTrajectory()
        #
        # self.left = EncoderFollower(leftTrajectory)
        # self.right = EncoderFollower(rightTrajectory)

        self.left.reset()
        self.right.reset()
        self.gyro_start = self.gyro.getAngle()
        #self.gyro.reset()

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

        lSegment = self.left.getSegment()
        rSegment = self.right.getSegment()

        l_encoder = self.leftEncoder.get()
        r_encoder = self.rightEncoder.get()

        if self.reverse:
            r_encoder = -r_encoder
            l_encoder = -l_encoder
            powerLeft = self.left.calculate(r_encoder)
            powerRight = self.right.calculate(l_encoder)
            current_gp = -self.gp
        else:
            powerLeft = self.left.calculate(l_encoder)
            powerRight = self.right.calculate(r_encoder)
            current_gp = self.gp

        desired_heading = pf.r2d(self.left.getHeading())
        turn, gyro_heading, angleDifference = self.gotoAngle(desired_heading, current_gp)

        if self.reverse:
            l = powerRight +turn
            r = powerLeft -turn
        else:
            l = -powerLeft+turn
            r = -powerRight-turn
        
        # ensure within -1..1
        absl = abs(l)
        absr = abs(r)
        maxm = max(absl, absr)
        if maxm > 1:
            if absl > absr:
                l = math.copysign(1, l)
                r = math.copysign(absr/absl, r)
            else:
                l = math.copysign(absl/absr, l)
                r = math.copysign(1, r)
        
        self.driveTrain.movePathFinder(l, r)

        if self.left.isFinished() or self.right.isFinished():
            self.running = False
            '''if abs(pf.boundHalfDegrees(angleDifference)) > 5:
                if self.location == 'MiddleExtraRightCube':
                    self.driveTrain.moveAngle(0.5, pf.boundHalfDegrees(desired_heading))
                else:
                    self.driveTrain.moveAngle(0.5, pf.boundHalfDegrees(-desired_heading))
            else:
                self.running = False'''

        l_distance_covered = ((l_encoder - self.left.cfg.initial_position) / 360.0) * math.pi * RobotMap.WHEEL_DIAMETER
        r_distance_covered = ((r_encoder - self.right.cfg.initial_position) / 360.0) * math.pi * RobotMap.WHEEL_DIAMETER

        # debugging
        data = [
            Timer.getFPGATimestamp(),

            l,
            l_encoder,
            l_distance_covered,
            lSegment.position,
            lSegment.velocity,

            r,
            r_encoder,
            r_distance_covered,
            rSegment.position,
            rSegment.velocity,

            gyro_heading,
            desired_heading,
            angleDifference,

            lSegment.x,
            lSegment.y,
            rSegment.x,
            rSegment.y,
        ]

        SmartDashboard.putNumberArray('pfdebug', data)

    def gotoAngle(self, desired_heading, current_gp):
        gyro_heading = -(self.gyro.getAngle() - self.gyro_start)
        angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
        turn = self.gp * angleDifference + (self.gd *
                ((angleDifference - self.angle_error) / self.dt))
        self.angle_error = angleDifference
        turn = max(min(turn, self.turn_limit), -self.turn_limit)
        return turn, gyro_heading, angleDifference

    def on_disable(self):
        self.running = False
