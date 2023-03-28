class TextBox():
    def __init__(self, canvas, x, y, text, size, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.create()

    def create(self):
        self.text = self.canvas.create_text((self.x,self.y), text=self.text, fill=self.color, font=("Inter-SemiBold", self.size))

    def delete(self):
        self.canvas.delete(self.text)