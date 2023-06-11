from PIL import ImageTk, Image

class Photo():
    def __init__(self, canvas, file_name, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y

        # select appropriate file path because VScode likes to be difficult
        self.file_name = "image/" + file_name + ".png"
        self.file_name2 = "../image/" + file_name + ".png"
        try:
            self.image_file = Image.open(self.file_name)
        except FileNotFoundError:
            self.image_file = Image.open(self.file_name2)

        self.canvas_image = ImageTk.PhotoImage(self.image_file)
        self.photo = self.canvas.create_image(self.x, self.y, image=self.canvas_image)

    def hide(self):
        self.canvas.itemconfigure(self.photo, state='hidden')

    def show(self):
        self.canvas.itemconfigure(self.photo, state='normal')
