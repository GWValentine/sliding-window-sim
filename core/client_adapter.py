class ClientAdapter:
    def __init__(self, send_buffer, send_window):
        self.send_buffer = send_buffer
        self.window = send_window
        self.pending_acks = {}

    def preSend(self, frame, current_time):
        if self.send_buffer.is_full():
            print(f"[{current_time}] sendBuffer Full")
            return
        
        self.send_buffer.add(frame)
        print(f"[{current_time}] queued frame {frame.ID}")

    def handle_ack(self, ack_id, current_time):
        print(f"[{current_time}] CLIENT received ACK {ack_id}")
        self.window.advance_ack(ack_id)

        # ACK received, so we can remove from pending timeouts
        if ack_id in self.pending_acks:
            del self.pending_acks[ack_id]

    def tick(self, current_time):
        # Check for timeouts
        expired = [fid for fid, exp in self.pending_acks.items() if current_time >= exp]
        for fid in expired:
            print(f"[{current_time}] TIMEOUT for frame {fid}, retransmitting")
            self.window.LFS = self.window.LAR
            del self.pending_acks[fid]

        # Try to send next frame
        frame = self.send_buffer.peek()
        if not frame:
            return None
        
        if frame.lose_frame:
            print(f"[{current_time}] frame {frame.ID} LOST (not sent)")
            self.send_buffer.remove()
            return
        
        if self.window.is_blocked():
            print(f"[{current_time}] send window BLOCKED")
            return
        
        # Send the frame
        frame.time_sent = current_time
        frame.time_expires = current_time + frame.timeout
        self.pending_acks[frame.ID] = frame.time_expires

        print(f"[{current_time}] SENT frame {frame.ID}, expires at {frame.time_expires}")

        self.window.LFS += 1
        self.send_buffer.remove()
        return frame

