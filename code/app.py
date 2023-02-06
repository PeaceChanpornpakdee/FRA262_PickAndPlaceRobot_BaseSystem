import tkinter as tk
from tkinter import ttk

from frame import MainFrame, FieldFrame, TestCanvas, Canvas
from color import Color

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Base System')

        # App window dimension
        window_width = 900
        window_height = 780

        # Find the center point
        center_x = int(self.winfo_screenwidth()/2 - window_width / 2)
        center_y = 0

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(bg=Color.darkgray)

if __name__ == "__main__":
    app = App()
    # frame = MainFrame(app)

    # s = ttk.Style()
    # s.configure('BW.TFrame', background=Color.white)
    # field = FieldFrame(app, 'BW.TFrame')

    # test = TestCanvas(app)

    # test2 = TestCanvas(app)

    cv = Canvas(app)

    app.mainloop()