import pathfinder as pf
import matplotlib.pyplot as plt
import RobotMap

points = [
    pf.Waypoint(0, 0, pf.d2r(0)),
    pf.Waypoint(7, -8, pf.d2r(0)),
    #pf.Waypoint(7.25, -7.75, pf.d2r(20)),
    #pf.Waypoint(7.5, -7.5, pf.d2r(30)),
    #pf.Waypoint(7.75, -7.25, pf.d2r(37)),
    pf.Waypoint(8, -7, pf.d2r(90))
]

info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC,
                               pf.SAMPLES_HIGH, RobotMap.dt, RobotMap.max_velocity, RobotMap.max_acceleration, RobotMap.max_jerk)

# Wheelbase Width = 0.5m
modifier = pf.modifiers.TankModifier(trajectory).modify(RobotMap.Width_Base)
# Do something with th Te new Trajectories...
leftTrajectory = modifier.getLeftTrajectory()
rightTrajectory = modifier.getRightTrajectory()

xValue = []
yValue = []
rangeValue = []
headingValue = []
num = 0

for i, j in zip(leftTrajectory, rightTrajectory):
    num += 1
    xValue.append(i.x)
    yValue.append(i.y)
    rangeValue.append(num)
    headingValue.append(i.heading)


plt.plot(rangeValue, xValue, 'r--', rangeValue, yValue, 'bs', rangeValue, headingValue, 'g^')
plt.show()
