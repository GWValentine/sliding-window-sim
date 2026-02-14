from core.buffers import Buffer
from core.windows import SendWindow, ReceiveWindow
from core.client_adapter import ClientAdapter
from core.server_adapter import ServerAdapter
from core.driver import Driver

def main():
    SWS = 5
    RWS = 5

    # Create Buffers
    send_buffer = Buffer(capacity=2 * SWS)
    rcv_buffer = Buffer(capacity=2 * SWS)

    # Create windows
    send_window = SendWindow(size=SWS)
    rcv_window = ReceiveWindow(size=RWS)

    # Create Adapters
    client = ClientAdapter(send_buffer, send_window)
    server = ServerAdapter(rcv_buffer, rcv_window)

    # Config file path
    config_path = "config/config1.txt"

    # Create Driver
    driver = Driver(client, server, config_path)
    driver.run()

    if __name__ == "__main__":
        main()