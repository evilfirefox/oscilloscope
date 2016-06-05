from tkinter import Tk, Frame
import _thread
from serial import Serial

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class Oscilloscope:
    data_x = [],
    data_y = []

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.chart = Figure(figsize=(5, 5), dpi=100)
        self.subplot = self.chart.add_subplot(1, 1, 1)
        # self.subplot.plot([1, 2, 3, 4, 5], [4.9, 0, 4.9, 0, 4.9])

        self.canvas = FigureCanvasTkAgg(self.chart, frame)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=2, column=1)

    def update_chart(self, data_x, data_y):
        self.subplot.clear()
        self.subplot.plot(data_x, data_y)
        self.canvas.draw()


root = Tk()
root.wm_title("Oscilloscope")
root.resizable(0, 0)

app = Oscilloscope(root)
root.mainloop()
