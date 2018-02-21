from wpilib import DoubleSolenoid

class OperateArm:

    armSolenoid = DoubleSolenoid

    def __init__(self):
        self.option = -1

    def setArm(self, option):
        self.option = option

    def execute(self):
        if self.option:
            self.armSolenoid.set(DoubleSolenoid.Value.kForward)
        else:
            self.armSolenoid.set(DoubleSolenoid.Value.kReverse)
