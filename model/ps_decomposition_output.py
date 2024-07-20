"""
    model of process output
"""


class DecompositionOutput:
    def __init__(self, channel, channel_suffix, visible, mask):
        self.channel = channel
        self.channel_suffix = channel_suffix
        self.visible = visible
        self.mask = mask
