class RoundRectangle():
    """
    Round Rectangle Class
    """
    def __init__(self, root_canvas, x, y, w, h, r, color):
        self.root_canvas = root_canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.color = color
        self.create()

    def create(self):
        x, y, w, h, r = self.x, self.y, self.w, self.h, self.r
        self.oval_1 = self.root_canvas.canvas.create_oval(x,       y,       x+2*r, y+2*r, fill=self.color, outline='')
        self.oval_2 = self.root_canvas.canvas.create_oval(x+w-2*r, y,       x+w,   y+2*r, fill=self.color, outline='')
        self.oval_3 = self.root_canvas.canvas.create_oval(x,       y+h-2*r, x+2*r, y+h,   fill=self.color, outline='')
        self.oval_4 = self.root_canvas.canvas.create_oval(x+w-2*r, y+h-2*r, x+w,   y+h,   fill=self.color, outline='')
        self.rec_1  = self.root_canvas.canvas.create_rectangle(x+r, y,   x+w-r, y+h,   fill=self.color, outline='')
        self.rec_2  = self.root_canvas.canvas.create_rectangle(x,   y+r, x+w,   y+h-r, fill=self.color, outline='')

    def delete(self):
        self.root_canvas.canvas.delete(self.oval_1)
        self.root_canvas.canvas.delete(self.oval_2)
        self.root_canvas.canvas.delete(self.oval_3)
        self.root_canvas.canvas.delete(self.oval_4)
        self.root_canvas.canvas.delete(self.rec_1)
        self.root_canvas.canvas.delete(self.rec_2)

class Oval():
    """
    Oval Class
    """
    def __init__(self, root_canvas, x, y, d, fill_color, outline_color):
        self.root_canvas = root_canvas
        self.x = x
        self.y = y
        self.d = d
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.create()

    def create(self):
        x, y, d = self.x, self.y, self.d
        self.oval = self.root_canvas.canvas.create_oval(x, y, x+d, y+d, fill=self.fill_color, outline=self.outline_color) 

    def delete(self):
        self.root_canvas.canvas.delete(self.oval)