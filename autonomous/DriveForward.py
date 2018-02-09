from magicbot import AutonomousStateMachine, timed_state
from components.DriveTrain import DriveTrain
from wpilib import ADXRS450_Gyro

class DriveForward(AutonomousStateMachine):

    MODE_NAME = "Drive Forward"
    DEFAULT = True

    driveTrain = DriveTrain
    gyro = ADXRS450_Gyro

    @timed_state(duration=3, first=True)
    def moveForward(self, initial_call):
        if initial_call:
            self.angle = self.gyro.getAngle()
        self.driveTrain.moveAngle(1, self.angle)
