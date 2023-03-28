class Oval():
    """
    Oval Class
    """
    def __init__(self, canvas, x, y, d, fill_color, outline_color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.d = d
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.create()

    def create(self):
        x, y, d = self.x, self.y, self.d
        self.oval = self.canvas.create_oval(x, y, x+d, y+d, fill=self.fill_color, outline=self.outline_color, width=2) 

    def delete(self):
        self.canvas.delete(self.oval)

class Rectangle():
    def __init__(self, canvas, x, y, w, h, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.create()

    def create(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        self.rectangle  = self.canvas.create_rectangle(x, y, x+w, y+h, fill=self.color, outline='')
    
    def delete(self):
        self.canvas.delete(self.rectangle)
    

class RoundRectangle():
    """
    Round Rectangle Class
    """
    def __init__(self, canvas, x, y, w, h, r, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.color = color
        self.create()

    def create(self):
        x, y, w, h, r = self.x, self.y, self.w, self.h, self.r
        self.oval_1 = Oval(self.canvas, x,       y,       2*r, fill_color=self.color, outline_color="")
        self.oval_2 = Oval(self.canvas, x+w-2*r, y,       2*r, fill_color=self.color, outline_color="")
        self.oval_3 = Oval(self.canvas, x,       y+h-2*r, 2*r, fill_color=self.color, outline_color="")
        self.oval_4 = Oval(self.canvas, x+w-2*r, y+h-2*r, 2*r, fill_color=self.color, outline_color="")
        self.rec_1  = Rectangle(self.canvas, x+r, y,   w-2*r, h,   self.color)
        self.rec_2  = Rectangle(self.canvas, x,   y+r, w,   h-2*r, self.color)

    def delete(self):
        self.oval_1.delete()
        self.oval_2.delete()
        self.oval_3.delete()
        self.oval_4.delete()
        self.rec_1.delete()
        self.rec_2.delete()