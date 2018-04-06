from pyfrc.physics import drivetrains
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
        self.left_distance = 0
        self.right_distance = 0
        self.WHEEL_DIAMETER = 0.5

        self.drivetrain = drivetrains.FourMotorDrivetrain()

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
        lf_motor = hal_data['pwm'][2]['value']*-1
        rf_motor = hal_data['pwm'][0]['value']*-1

        speed, rotation = self.drivetrain.get_vector(lr_motor, rr_motor, lf_motor, rf_motor)
        #if abs(speed) > 0:
        #    rotation -= 0.3
        self.physics_controller.drive(speed, rotation, tm_diff)
        self.left_distance += (self.drivetrain.l_speed * tm_diff)
        self.right_distance += (self.drivetrain.r_speed * tm_diff)
        self.left_counter = self.left_distance / (RobotMap.WHEEL_DIAMETER * math.pi / 360)
        self.right_counter = self.right_distance / (RobotMap.WHEEL_DIAMETER * math.pi / 360)

        hal_data['encoder'][0]['count'] = int(self.left_counter)
        hal_data['encoder'][1]['count'] = int(self.right_counter)

        #print(self.left_counter, self.right_counter)
