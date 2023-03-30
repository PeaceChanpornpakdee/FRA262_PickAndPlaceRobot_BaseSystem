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

    def hide(self):
        self.canvas.itemconfigure(self.oval, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.oval, state='normal')
    
    def activate(self, active_color):
        self.canvas.itemconfigure(self.oval, fill=active_color)

    def deactivate(self, inactive_color):
        self.canvas.itemconfigure(self.oval, fill=inactive_color)


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
        self.rect  = self.canvas.create_rectangle(x, y, x+w, y+h, fill=self.color, outline='')
    
    def delete(self):
        self.canvas.delete(self.rect)

    def hide(self):
        self.canvas.itemconfigure(self.rect, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.rect, state='normal')

    def activate(self, active_color):
        self.canvas.itemconfigure(self.rect, fill=active_color)

    def deactivate(self, inactive_color):
        self.canvas.itemconfigure(self.rect, fill=inactive_color)
    

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

    def hide(self):
        self.oval_1.hide()
        self.oval_2.hide()
        self.oval_3.hide()
        self.oval_4.hide()
        self.rec_1.hide()
        self.rec_2.hide()

    def show(self):
        self.oval_1.show()
        self.oval_2.show()
        self.oval_3.show()
        self.oval_4.show()
        self.rec_1.show()
        self.rec_2.show()

    def activate(self, active_color):
        self.oval_1.activate(active_color)
        self.oval_2.activate(active_color)
        self.oval_3.activate(active_color)
        self.oval_4.activate(active_color)
        self.rec_1.activate(active_color)
        self.rec_2.activate(active_color)

    def deactivate(self, inactive_color):
        self.oval_1.deactivate(inactive_color)
        self.oval_2.deactivate(inactive_color)
        self.oval_3.deactivate(inactive_color)
        self.oval_4.deactivate(inactive_color)
        self.rec_1.deactivate(inactive_color)
        self.rec_2.deactivate(inactive_color)
