import csv
from core.frame import Frame

class Driver:
    def __init__(self, client, server, config_path):
        self.client = client
        self.server = server
        self.config_path = config_path
        self.current_time = 0

        self.in_flight_frame = None
        self.in_flight_ack = None

        self.commands = self.load_config()

    def load_config(self):
        commands = []
        with open(self.config_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                commands.append(row)
        return commands

    def run(self):
        for row in self.commands:
            self.current_time = int(row["time"])
            cmd = row["cmd"]

            print(f"\n===== TIME {self.current_time} =====")

            if cmd == "preSend":
                frame = Frame(
                    ID=int(row["ID"]),
                    timeout=3,
                    lose_frame=(row["loseFrame"] == "true"),
                    lose_ack=(row["loseACK"] == "true")
                )
                self.client.preSend(frame, self.current_time)
            
            elif cmd == "tick":
                #Switched to Check timeout last
                if self.in_flight_ack is not None:
                    self.client.handle_ack(self.in_flight_ack, self.current_time)
                    self.in_flight_ack = None

                sent_frame = self.client.tick(self.current_time)
                if sent_frame:
                    self.in_flight_frame = sent_frame



            elif cmd == "tock":
                if self.in_flight_frame:
                    ack = self.server.tock(self.in_flight_frame, self.current_time)
                    self.in_flight_frame = None

                    if ack is not None:
                        self.in_flight_ack = ack

            elif cmd == "rcv":
                self.server.rcv(self.current_time)