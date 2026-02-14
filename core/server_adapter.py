class ServerAdapter:
    def __init__(self, rcv_buffer, rcv_window):
        self.rcv_buffer = rcv_buffer
        self.window = rcv_window

    def tock(self, frame, current_time):
        if frame is None:
            return
        
        if self.window.is_blocked(frame.ID):
            print(f"[{current_time}] receive window BLOCKED")
            return
        
        print(f"[{current_time}] RECEIVED frame {frame.ID}")

        self.rcv_buffer.add(frame)
        self.window.LFR += 1
        self.window.LAF = self.window.LFR + self.window.size

        if not frame.lose_ack:
            print(f"[{current_time}] ACK frame {frame.ID}")
            return frame.ID # returning ACK to client
        else:
            print(f"[{current_time}] ACK for {frame.ID} LOST")
            return None
        

    def rcv(self, current_time):
        frame = self.rcv_buffer.remove()
        if frame:
            print(f"{[current_time]} APP consumed frame {frame.ID}")
        else:
            print(f"{[current_time]} rcvBuffer EMPTY")