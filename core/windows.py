class SendWindow:
    def __init__(self, size):
        self.size = size
        self.LFS = 0
        self.LAR = 0

    def is_blocked(self):
        return (self.LFS - self.LAR) >= self.size
    
    def advance_ack(self, ack_id):
        if ack_id > self.LAR:
            self.LAR = 