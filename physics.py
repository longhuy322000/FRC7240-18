from pyfrc.physics import drivetrains
import math

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
        self.physics_controller.add_device_gyro_channel('adxrs450_spi_0_angle')
        self.left_distance = 0
        self.right_distance = 0
        self.DIAMETER_WHEEL = 0.4375

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

        speed, rotation, leftSpeed, rightSpeed = drivetrains.four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        #if abs(speed) > 0:
        #    rotation -= 0.3
        self.physics_controller.drive(speed, rotation, tm_diff)
        self.left_distance += abs(leftSpeed * tm_diff)
        self.right_distance += abs(rightSpeed * tm_diff)
        self.left_counter = self.left_distance / (self.DIAMETER_WHEEL * math.pi)
        self.right_counter = self.right_distance / (self.DIAMETER_WHEEL * math.pi)

        hal_data['encoder'][0]['counter'] = self.left_counter
        hal_data['encoder'][1]['counter'] = self.right_counter
