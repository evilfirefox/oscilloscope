from serial import Serial
import _thread


class HardwareInteraction:
    DEFAULT_BAUDRATE = 9600
    DEFAULT_TIMEOUT = .1

    socket = Serial()
    input_handler = 0

    def __init__(self, input_handler):
        self.input_handler = input_handler

    def connect(self, port, baudrate=DEFAULT_BAUDRATE, timeout=DEFAULT_TIMEOUT):
        if self.socket.is_open:
            self.socket.close()
        self.socket.port = port
        self.socket.baudrate = baudrate
        self.socket.timeout = timeout
        self.socket.open()
        _thread.start_new(self.poll, ())

    def poll(self):
        while True:
            data = self.socket.readline()
            if data:
                self.input_handler(data.decode('utf-8'))
