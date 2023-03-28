class TextBox():
    def __init__(self, root_canvas, x, y, text, size, color):
        self.x = x
        self.y = y
        self.canvas = root_canvas.canvas
        self.text = text
        self.size = size
        self.color = color
        self.create()

    def create(self):
        self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=("Inter-SemiBold", self.size))