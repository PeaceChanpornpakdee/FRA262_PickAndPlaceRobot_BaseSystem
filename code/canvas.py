import tkinter as tk
from PIL import ImageTk, Image
from color import Color
from calculation import *

class Canvas():
    """
    Canvas class
    """
    def __init__(self, container, width, height, padding):
        # self.canvas = tk.Canvas(container, width=width, height=height, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge', cursor='sb_down_arrow')
        self.canvas = tk.Canvas(container, width=width, height=height, bg=Color.darkgray, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(pady=padding)
        self.create_round_rectangle("TopLeft", 0, 0, width, height, 20, Color.white)

    def create_round_rectangle(self, mode, x, y, w, h, r, color):
        if mode == "Center":
            x = x - w/2
            y = y - h/2
        self.canvas.create_oval(x,       y,       x+2*r, y+2*r, fill=color, outline='')
        self.canvas.create_oval(x+w-2*r, y,       x+w,   y+2*r, fill=color, outline='')
        self.canvas.create_oval(x,       y+h-2*r, x+2*r, y+h,   fill=color, outline='')
        self.canvas.create_oval(x+w-2*r, y+h-2*r, x+w,   y+h,   fill=color, outline='')
        self.canvas.create_rectangle(x+r, y,   x+w-r, y+h,   fill=color, outline='')
        self.canvas.create_rectangle(x,   y+r, x+w,   y+h-r, fill=color, outline='')

    def create_grid(self, x, y, row, column, color):
        """
        Function to draw a field grid

        Parameters:
            x (int)      : top left origin x
            y (int)      : top left origin y
            row (int)    : number of rows
            column (int) : number of columns
            color (str)  : color code 
        """
        for r in range(row+1):
            self.canvas.create_line((x+560-8*r, y+280+120-4*r), (x+560+240-8*r, y+280-4*r), width=1, fill=color)

        for c in range(column+1):
            self.canvas.create_line((x+8*c, y+120-4*c), (x+560+8*c, y+120+280-4*c), width=1, fill=color)

        self.canvas.create_line((x+560-8*35, y+280+120-4*35), (x+560+240-8*35, y+280-4*35), width=2, fill=color)
        self.canvas.create_line((x+8*15, y+120-4*15), (x+560+8*15, y+120+280-4*15), width=2, fill=color)

    def create_textbox(self, x, y, text, size, color):
        self.canvas.create_text((x,y), text=text, fill=color, font=("Inter-SemiBold", size))

    def create_photo(self, file_name, x, y):
        file = "image/" + file_name + ".png"
        image = Image.open(file)
        self.canvas.image = ImageTk.PhotoImage(image)
        self.canvas.create_image(x, y, image=self.canvas.image)

    def create_tray(self, origin_x, origin_y, orientation):
        tray_points = map_tray_points(origin_x, origin_y, 6, 5, 0.5, orientation)
        self.canvas.create_polygon(*tray_points["bottom_tray"], fill=Color.gray, outline="")
        self.canvas.create_polygon(*tray_points["top_tray"],    fill=Color.lightgray, outline="")
        self.canvas.create_polygon(*tray_points["left_wall"],   fill=Color.middlegray, outline="")
        self.canvas.create_polygon(*tray_points["right_wall"],  fill=Color.gray, outline="")
        for row in range(3):
            for column in range(3):
                self.canvas.create_oval(*(tray_points["holes"][row][column]), fill=Color.gray, outline='')

    def create_navigator(self, grid_x, grid_y, grid_z):

        navigator_points = map_navigator_points(grid_x, grid_y, grid_z)

        self.laser_on = True
        if self.laser_on:
            pixel_x = navigator_points["navigator_tip"][0]
            pixel_y = navigator_points["navigator_tip"][1]
            points = (
                (pixel_x, pixel_y - 5),
                (pixel_x, pixel_y + grid_z*8),
            )
            self.canvas.create_line(*points, width=2, fill=Color.red)

        self.canvas.create_polygon(*navigator_points["navigator_top"], fill="#FFD18C", outline="")
        self.canvas.create_polygon(*navigator_points["navigator_left"], fill="#FFB545", outline="")
        self.canvas.create_polygon(*navigator_points["navigator_right"], fill="#EAA031", outline="")
