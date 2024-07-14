"""
    model of decomposition output
"""


class DecompositionOutput:
    def __init__(self, channel, channel_suffix, visible_suffix, mask_suffix):
        self.channel = channel
        self.channel_suffix = channel_suffix
        self.visible_suffix = visible_suffix
        self.mask_suffix = mask_suffix
