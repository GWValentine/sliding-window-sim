class ClientAdapter:
    def __init__(self, send_buffer, send_window):
        self.send_buffer = send_buffer
        self.window = send_window
        self.pending_acks = {}
        self.backup_frames = {} # Frames that may need to be resent

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

        #Also delete backup Frame
        if ack_id in self.backup_frames:
            del self.backup_frames[ack_id]

    def tick(self, current_time):
        # Check for timeouts
        expired = [fid for fid, exp in self.pending_acks.items() if current_time > exp]
        
        #Changed >= to > to give it the tick, ie 2 second timeout is not 1 second
        ''' - changing some logic
        for fid in expired:
            print(f"[{current_time}] TIMEOUT for frame {fid}, retransmitting")
            self.window.LFS = self.window.LAR
            del self.pending_acks[fid]
        '''

        if expired: #Retransmit oldest frame first
            fid = sorted(expired)[0]
            print(f"[{current_time}] TIMEOUT for frame {fid}, run it back")

            frame = self.backup_frames[fid]
            frame.time_expires = current_time + frame.timeout
            self.pending_acks[fid] = frame.time_expires
            
            return frame #Give driver backup frame

        # Try to send next frame
        frame = self.send_buffer.peek()
        if not frame:
            return None
        
        if self.window.is_blocked():
            print(f"[{current_time}] send window BLOCKED")
            return
        
        # Send the frame
        frame.time_sent = current_time
        frame.time_expires = current_time + frame.timeout
        self.pending_acks[frame.ID] = frame.time_expires

        self.window.LFS += 1
        self.send_buffer.remove()
        self.backup_frames[frame.ID] = frame #Save Backup Frame

        # We have to act like we send the fame, sim logic after
        if frame.lose_frame:
            print(f"[{current_time}] frame {frame.ID} LOST (not sent)")
            return None #The frame never sent, but client thinks so

        # Norml Sending
        print(f"[{current_time}] SENT frame {frame.ID}, expires at {frame.time_expires}")
        return frame

