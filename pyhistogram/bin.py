"""Definition of the Bin class"""


class _Bin(object):
    def __init__(self, lower_edge, upper_edge, content=0):
        # check values
        if lower_edge >= upper_edge:
            raise ValueError('Lower edge has a large value than upper edge')
        self.lower_edge = lower_edge
        self.upper_edge = upper_edge
        self.center = lower_edge + (upper_edge - lower_edge) / 2.0
        self.content = content

