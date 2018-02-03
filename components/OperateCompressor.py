import wpilib
from wpilib import DoubleSolenoid, Compressor

class OperateCompressor:

    compressor = Compressor

    def __init__(self):
        self.active = False

    def setCompressor(self, active):
        self.active = active

    def execute(self):
        if active:
            self.compressor.start()
        else:
            self.compressor.stop()
