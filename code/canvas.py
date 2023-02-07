import tkinter as tk
import math
from PIL import ImageTk, Image
from color import Color

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
        self.grid_x = x
        self.grid_y = y
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

    def map_3D_to_2D(self, x, y, z):
        pixel_x =   8*(x+15) - 8*(y+35) + 560        + self.grid_x
        pixel_y = -(4*(x+15) + 4*(y+35) - 400 + 8*z) + self.grid_y
        print(pixel_x, pixel_y)
        return pixel_x, pixel_y

    def map_tray_points(self, x, y, w, h, theta):
        """
        w = 6
        h = 5
        """
        r = (w**2 + h**2) ** 0.5
        theta = math.radians(theta)
        tray_theta = math.atan(w/h)

        point_1 = (x, y)
        point_2 = (x + w*math.cos(theta), x - w*math.sin(theta))
        point_3 = (r * math.sin(theta+tray_theta), r * math.cos(theta+tray_theta))
        point_4 = (y + h*math.sin(theta), y + h*math.cos(theta))

        print(point_1, point_2, point_3, point_4)

        return (point_1, point_2, point_3, point_4)

    def create_tray(self, origin_x, origin_y, orientation):
        """
        Function to draw a field grid

        Parameters:
            x (float)   : tray origin x
            y (float)   : tray origin y
            orientation (float) : tray orientation in degree
        """

        #Bottom tray
        points = self.map_tray_points(origin_x, origin_y, 6, 5, orientation)
        pixels = (
            self.map_3D_to_2D(points[0][0], points[0][1], 0),
            self.map_3D_to_2D(points[1][0], points[1][1], 0),
            self.map_3D_to_2D(points[2][0], points[2][1], 0),
            self.map_3D_to_2D(points[3][0], points[3][1], 0),
        )
        self.canvas.create_polygon(*pixels, fill=Color.gray, outline="")

    def create_navigator(self, x, y, z):

        x,y = self.map_3D_to_2D(x, y, z)

        self.laser_on = True
        if self.laser_on:
            self.canvas.create_line((x, y-5), (x, y+z*8), width=2, fill=Color.red)

        points = (
            (x,    y-16),
            (x-16, y-24),
            (x,    y-32),
            (x+16, y-24),
        )
        self.canvas.create_polygon(*points, fill="#FFD18C", outline="")

        points = (
            (x,    y),
            (x-16, y-24),
            (x,    y-16),
        )
        self.canvas.create_polygon(*points, fill="#FFB545", outline="")

        points = (
            (x,    y),
            (x+16, y-24),
            (x,    y-16),
        )
        self.canvas.create_polygon(*points, fill="#EAA031", outline="")




    