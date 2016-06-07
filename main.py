import sys
import pprint
import _thread
from tkinter import Tk, Frame, Entry, Button, Label
from tkinter.constants import W, E
from hw_interaction import HardwareInteraction

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class Oscilloscope:
    DELTA_THRESHOLD = 50
    data = {}
    time_index = 0
    device = 0
    log_file = 0
    device_port = 0
    log_path = 0
    start_button = 0
    chart = 0
    subplot = 0
    canvas = 0

    def __init__(self, master):
        self.device = HardwareInteraction(self.handle_serial)

        frame = Frame(master)
        frame.pack()

        self.configure_frame(frame)

    def configure_frame(self, frame):
        Label(frame, text="Device port").grid(row=0, column=0)
        self.device_port = Entry(frame)
        self.device_port.insert(0, "COM3")
        self.device_port.grid(row=0, column=1, sticky=W + E)

        Label(frame, text="Log path").grid(row=1, column=0)
        self.log_path = Entry(frame)
        self.log_path.insert(0, "test.log")
        self.log_path.grid(row=1, column=1, sticky=W + E)

        self.start_button = Button(frame, text="Start", command=self.start_operations)
        self.start_button.grid(row=2, column=0, sticky=W + E)

        self.start_button = Button(frame, text="Stop&close", command=self.stop_operations)
        self.start_button.grid(row=2, column=1, sticky=W + E)

        self.chart = Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.chart.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.chart, frame)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2)

    def start_operations(self):
        self.device.connect(port=self.device_port.get(), baudrate=19200)
        self.log_file = open(self.log_path.get(), 'a')

    def stop_operations(self):
        self.log_file.close()
        sys.exit(0)

    def update_chart(self, data):
        self.subplot.clear()
        self.subplot.plot(sorted(data.keys()), list(data.values()))
        self.canvas.draw()

    def handle_serial(self, data):
        self.data[self.time_index] = float(data)
        self.time_index += 1

        if len(self.data) > self.DELTA_THRESHOLD:
            i = 0
            data_to_log = {}
            for k, v in self.data.items():
                if i < self.DELTA_THRESHOLD:
                    data_to_log[k] = v
                i += 1
            for k in data_to_log.keys():
                del(self.data[k])
            _thread.start_new(self.log_data, (data_to_log,))

        self.update_chart(self.data)

    def log_data(self, data_to_log):
        for k, v in data_to_log.items():
            self.log_file.write("{0}: {1}\n".format(str(k).zfill(10), str(v)))


root = Tk()
root.wm_title("Oscilloscope")
root.resizable(0, 0)

app = Oscilloscope(root)
root.mainloop()
