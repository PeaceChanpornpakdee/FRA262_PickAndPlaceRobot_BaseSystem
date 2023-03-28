import tkinter as tk
from PIL import ImageTk, Image
from components.color import Color

class Canvas():
    """
    Canvas class
    """
    def __init__(self, container, width, height, padding):
        # self.canvas = tk.Canvas(container, width=width, height=height, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge', cursor='sb_down_arrow')
        self.canvas = tk.Canvas(container, width=width, height=height, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(pady=padding)

    def create_textbox(self, x, y, text, size, color):
        self.canvas.create_text((x,y), text=text, fill=color, font=("Inter-SemiBold", size))

    def create_photo(self, file_name, x, y):
        file = "image/" + file_name + ".png"
        image = Image.open(file)
        self.canvas.image = ImageTk.PhotoImage(image)
        self.canvas.create_image(x, y, image=self.canvas.image)



    def create_rectangle_button(self, x, y, w, h, r, button_color, text, text_size, text_color, function):
        self.create_round_rectangle(x, y, w, h, r, button_color)
        self.create_textbox(x+w/2, y+h/2, text, text_size, text_color)
        self.click_area = self.create_click_area(x, y, w, h, "rectangle")
        self.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", function)

    # def create_radio_button(self, x, y, r, button_color, status, function):
    #     if status == "active":
    #         self.canvas.create_oval(x, y, x+r, y+r, fill="", outline=button_color, width=2)
    #         self.canvas.create_oval(x+4, y+4, x+r-4, y+r-4, fill=button_color, outline="")
    #     elif status == "inactive":
    #         self.canvas.create_oval(x, y, x+r, y+r, fill="", outline=Color.lightgray, width=2)
    #     self.click_area = self.create_click_area(x, y, r, r, "oval")
    #     self.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", function)
