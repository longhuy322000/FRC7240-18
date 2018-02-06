from wpilib import Compressor

class OperateCompressor:

    compressor = Compressor

    def __init__(self):
        self.active = False

    def setCompressor(self, active):
        self.active = active

    def execute(self):
        if self.active:
            self.compressor.start()
        else:
            self.compressor.stop()
