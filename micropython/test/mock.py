from lib.core import NUM_OUTS


class MockOutput:
    def __init__(self):
        self.reset()

    def output(self, index, value):
        if (index < 0 or index >= NUM_OUTS):
            raise IndexError("invalid output index %d" % index)
        self.calls.append((index, value))

    def reset(self):
        self.calls = []
