class Frame:
    def __init__(self, ID, timeout, lose_frame, lose_ack):
        self.ID = ID
        self.timeout = timeout
        self.lose_frame = lose_frame
        self.lose_ack = lose_ack

        self.time_sent = None
        self.time_expires = None
        