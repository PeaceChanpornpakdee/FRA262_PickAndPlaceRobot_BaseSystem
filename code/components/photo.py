from PIL import ImageTk, Image

class Photo():
    def __init__(self, canvas, file_name, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.file_name = file_name
        file = "image/" + self.file_name + ".png"
        image_file = Image.open(file)
        self.canvas.image = ImageTk.PhotoImage(image_file)
        self.photo = self.canvas.create_image(self.x, self.y, image=self.canvas.image)