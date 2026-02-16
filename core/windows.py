class SendWindow:
    def __init__(self, size):
        self.size = size
        self.LFS = 0
        self.LAR = 0

    def is_blocked(self):
        # If not enough ACKS have been sent back, return true
        return (self.LFS - self.LAR) >= self.size
    
    # LAR goes based off of most recently received ACK
    def advance_ack(self, ack_id):
        if ack_id > self.LAR:
            self.LAR = ack_id

class ReceiveWindow:
    def __init__(self, size):
        self.size = size
        self.LFR = 0
        self.LAF = size

    def is_blocked(self, incoming_id):
        # If incoming frame is beyond acceptable window
        return incoming_id <= self.LFR or incoming_id > self.LAF