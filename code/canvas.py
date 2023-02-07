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
        self.pixel_grid_offset_x = x
        self.pixel_grid_offset_y = y
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

    def map_3D_to_2D(self, grid_x, grid_y, grid_z):
        pixel_x = self.pixel_grid_offset_x +  8*(grid_x+15) - 8*(grid_y+35) + 560
        pixel_y = self.pixel_grid_offset_y - (4*(grid_x+15) + 4*(grid_y+35) - 400 + 8*grid_z)
        return pixel_x, pixel_y

    def map_tray_points(self, grid_x, grid_y, tray_width, tray_height, tray_thick, orientation):
        """
        w = 6
        h = 5
        """

        tray_diagonal = (tray_width**2 + tray_height**2) ** 0.5
        theta = math.radians(orientation)
        tray_theta = math.atan(tray_width / tray_height)

        tray_points = {
            "bottom_tray" : (
                self.map_3D_to_2D( grid_x, grid_y, 0 ),
                self.map_3D_to_2D( grid_x + tray_width    * math.cos(theta),            grid_y - tray_width    * math.sin(theta),            0 ),
                self.map_3D_to_2D( grid_x + tray_diagonal * math.sin(theta+tray_theta), grid_y + tray_diagonal * math.cos(theta+tray_theta), 0 ),
                self.map_3D_to_2D( grid_x + tray_height   * math.sin(theta),            grid_y + tray_height   * math.cos(theta),            0 ),
            ),
            "top_tray" : (
                self.map_3D_to_2D( grid_x, grid_y, tray_thick ),
                self.map_3D_to_2D( grid_x + tray_width    * math.cos(theta),            grid_y - tray_width    * math.sin(theta), tray_thick ),
                self.map_3D_to_2D( grid_x + tray_diagonal * math.sin(theta+tray_theta), grid_y + tray_diagonal * math.cos(theta+tray_theta), tray_thick ),
                self.map_3D_to_2D( grid_x + tray_height   * math.sin(theta),            grid_y + tray_height   * math.cos(theta), tray_thick )
            ),
        }

        if orientation <= 45:
            left_side  = (3, 0)
            right_side = (0, 1) 
        elif orientation <= 135:
            left_side  = (0, 1)
            right_side = (1, 2) 
        elif orientation <= 225:
            left_side  = (1, 2)
            right_side = (2, 3) 
        elif orientation <= 315:
            left_side  = (2, 3)
            right_side = (3, 0) 
        else:
            left_side  = (3, 0)
            right_side = (0, 1) 

        tray_points["left_wall"] = ( 
            tray_points["bottom_tray"][left_side[0]], 
            tray_points["bottom_tray"][left_side[1]], 
            tray_points["top_tray"][left_side[1]], 
            tray_points["top_tray"][left_side[0]]
        )
        tray_points["right_wall"] = ( 
            tray_points["bottom_tray"][right_side[0]], 
            tray_points["bottom_tray"][right_side[1]], 
            tray_points["top_tray"][right_side[1]], 
            tray_points["top_tray"][right_side[0]]
        )

        return tray_points


    def create_tray(self, origin_x, origin_y, orientation):
        """
        Function to draw a field grid

        Parameters:
            x (float)   : tray origin x
            y (float)   : tray origin y
            orientation (float) : tray orientation in degree
        """

        tray_points = self.map_tray_points(origin_x, origin_y, 6, 5, 0.5, orientation)
        self.canvas.create_polygon(*tray_points["bottom_tray"], fill=Color.gray, outline="")
        self.canvas.create_polygon(*tray_points["top_tray"],    fill=Color.lightgray, outline="")
        self.canvas.create_polygon(*tray_points["left_wall"],   fill=Color.middlegray, outline="")
        self.canvas.create_polygon(*tray_points["right_wall"],  fill=Color.gray, outline="")

    def map_navigator_points(self, grid_x, grid_y, grid_z):
        pixel_x, pixel_y = self.map_3D_to_2D(grid_x, grid_y, grid_z)

        navigator_points = {
            "navigator_tip" : (pixel_x, pixel_y),
            "navigator_top" : (
                (pixel_x,      pixel_y - 16),
                (pixel_x - 16, pixel_y - 24),
                (pixel_x,      pixel_y - 32),
                (pixel_x + 16, pixel_y - 24),
            ),
            "navigator_left" : (
                (pixel_x,      pixel_y),
                (pixel_x - 16, pixel_y - 24),
                (pixel_x,      pixel_y - 16),
            ),
            "navigator_right" : (
                (pixel_x,      pixel_y),
                (pixel_x + 16, pixel_y - 24),
                (pixel_x,      pixel_y - 16),
            )
        }

        return navigator_points

    def create_navigator(self, grid_x, grid_y, grid_z):

        navigator_points = self.map_navigator_points(grid_x, grid_y, grid_z)

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
