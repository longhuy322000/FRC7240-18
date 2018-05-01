from pyfrc.physics import tankmodel, motor_cfgs
from pyfrc.physics.units import units

import math
import RobotMap

class PhysicsEngine(object):
    '''
       Simulates a 4-wheel robot using Tank Drive joystick control
    '''


    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        '''

        self.physics_controller = physics_controller
        self.physics_controller.add_device_gyro_channel('navxmxp_spi_4_angle')
        
        bumper_width = 3.25*units.inch
        robot_wheelbase = 22*units.inch
        robot_width = 23*units.inch + bumper_width*2
        robot_length = 32*units.inch + bumper_width*2
        wheel_diameter = 6*units.inch
        
        robot_mass = 90 * units.pounds
        
        self.drivetrain = tankmodel.TankModel.theory(motor_cfgs.MOTOR_CFG_CIM,
                                                     robot_mass, 10.71, 2,
                                                     robot_wheelbase,
                                                     robot_width,
                                                     robot_length,
                                                     wheel_diameter)

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        lr_motor = hal_data['pwm'][3]['value']*-1
        rr_motor = hal_data['pwm'][1]['value']*-1
        #lf_motor = hal_data['pwm'][2]['value']*-1
        #rf_motor = hal_data['pwm'][0]['value']*-1

        x, y, angle = self.drivetrain.get_distance(lr_motor, rr_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
        
        self.left_counter = self.drivetrain.l_position / (RobotMap.WHEEL_DIAMETER * math.pi / 360)
        self.right_counter = self.drivetrain.r_position / (RobotMap.WHEEL_DIAMETER * math.pi / 360)

        hal_data['encoder'][0]['count'] = int(self.left_counter)
        hal_data['encoder'][1]['count'] = int(self.right_counter)

        #print(self.left_counter, self.right_counter)
