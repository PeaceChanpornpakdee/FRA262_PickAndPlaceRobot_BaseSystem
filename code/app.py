import tkinter as tk

from frame import MainFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('My Awesome App')
        self.geometry('300x100')

if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    app.mainloop()