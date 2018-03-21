from wpilib import DoubleSolenoid

class OperateArm:

    armSolenoid = DoubleSolenoid

    def __init__(self):
        self.option = 'up'

    def setArm(self, option):
        self.option = option

    def execute(self):
        if self.option == 'up':
            self.armSolenoid.set(DoubleSolenoid.Value.kReverse)
        else:
            self.armSolenoid.set(DoubleSolenoid.Value.kForward)
