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
        self.create_round_rectangle(0, 0, width, height, 20, Color.whitegray)

    def create_round_rectangle(self, x, y, w, h, r, color):
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

    def create_rectangle_button(self, x, y, w, h, r, button_color, text, text_size, text_color, function):
        self.create_round_rectangle(x, y, w, h, r, button_color)
        self.create_textbox(x+w/2, y+h/2, text, text_size, text_color)
        self.click_area = self.create_click_area(x, y, w, h, "rectangle")
        self.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", function)

    def create_radio_button(self, x, y, r, button_color, status, function):
        if status == "active":
            self.canvas.create_oval(x, y, x+r, y+r, fill="", outline=button_color, width=2)
            self.canvas.create_oval(x+4, y+4, x+r-4, y+r-4, fill=button_color, outline="")
        elif status == "inactive":
            self.canvas.create_oval(x, y, x+r, y+r, fill="", outline=Color.lightgray, width=2)
        self.click_area = self.create_click_area(x, y, r, r, "oval")
        self.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", function)

    def create_target_point(self, grid_x, grid_y):
        target_points = map_target_points(grid_x, grid_y)
        self.canvas.create_oval(*target_points["inner_oval"], fill=Color.blue, outline='')
        self.canvas.create_oval(*target_points["outer_oval"], fill='', outline=Color.blue, width=2)
        for i in range(4):
            self.canvas.create_line(*target_points["tick"][i], fill=Color.blue, width=2)



class Tray():
    """
    Tray class
    """
    def __init__(self, root_canvas):
        self.root_canvas = root_canvas
        self.origin_x = 0
        self.origin_y = 0
        self.orientation = 0
        self.create_tray()

    def create_tray(self):
        tray_points = self.map_tray_points(self.origin_x, self.origin_y, 6, 5, 0.5, self.orientation)
        self.tray_bottom = self.root_canvas.canvas.create_polygon(*tray_points["bottom_tray"], fill=Color.gray, outline="")
        self.tray_top    = self.root_canvas.canvas.create_polygon(*tray_points["top_tray"],    fill=Color.lightgray, outline="")
        self.tray_left   = self.root_canvas.canvas.create_polygon(*tray_points["left_wall"],   fill=Color.middlegray, outline="")
        self.tray_right  = self.root_canvas.canvas.create_polygon(*tray_points["right_wall"],  fill=Color.gray, outline="")
        self.tray_holes  = []
        for row in range(3):
            for column in range(3):
                self.tray_holes.append(self.root_canvas.canvas.create_oval(*(tray_points["holes"][row][column]), fill=Color.gray, outline=''))

    def clear_tray(self):
        self.root_canvas.canvas.delete(self.tray_top)
        self.root_canvas.canvas.delete(self.tray_bottom)
        self.root_canvas.canvas.delete(self.tray_left)
        self.root_canvas.canvas.delete(self.tray_right)
        for i in range(9):
            self.root_canvas.canvas.delete(self.tray_holes[i])

    def map_tray_points(self, grid_x, grid_y, tray_width, tray_height, tray_thick, orientation):
        tray_diagonal = (tray_width**2 + tray_height**2) ** 0.5
        theta = math.radians(orientation)
        tray_theta = math.atan(tray_width / tray_height)

        tray_points = {
            "bottom_tray" : (
                map_3D_to_2D( grid_x, grid_y, 0 ),
                map_3D_to_2D( grid_x + tray_width    * math.cos(theta),            grid_y - tray_width    * math.sin(theta),            0 ),
                map_3D_to_2D( grid_x + tray_diagonal * math.sin(theta+tray_theta), grid_y + tray_diagonal * math.cos(theta+tray_theta), 0 ),
                map_3D_to_2D( grid_x + tray_height   * math.sin(theta),            grid_y + tray_height   * math.cos(theta),            0 ),
            ),
            "top_tray" : (
                map_3D_to_2D( grid_x, grid_y, tray_thick ),
                map_3D_to_2D( grid_x + tray_width    * math.cos(theta),            grid_y - tray_width    * math.sin(theta), tray_thick ),
                map_3D_to_2D( grid_x + tray_diagonal * math.sin(theta+tray_theta), grid_y + tray_diagonal * math.cos(theta+tray_theta), tray_thick ),
                map_3D_to_2D( grid_x + tray_height   * math.sin(theta),            grid_y + tray_height   * math.cos(theta), tray_thick )
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

        hole_centers = []
        for row in range(3):
            hole_centers.append([])
            for column in range(3):
                hole_tray_x = 1 + 2*column
                hole_tray_y = 1 + 1.5*row
                hole_diagonal = (hole_tray_x**2 + hole_tray_y**2) ** 0.5
                hole_theta = math.atan(hole_tray_x / hole_tray_y)
                hole_centers[row].append( map_3D_to_2D( grid_x + hole_diagonal * math.sin(theta+hole_theta), grid_y + hole_diagonal * math.cos(theta+hole_theta), tray_thick ), )

        hole_points = []
        for row in range(3):
            hole_points.append([])
            for column in range(3):
                hole_center_point = hole_centers[row][column]
                hole_points[row].append((
                    (hole_center_point[0]-4, hole_center_point[1]+2),
                    (hole_center_point[0]+4, hole_center_point[1]-2),
                ))

        tray_points["holes"] = hole_points

        return tray_points



class Navigator():
    """
    Navigator class
    """
    def __init__(self, root_canvas, grid_x, grid_y, grid_z):
        self.root_canvas = root_canvas
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_z = grid_z
        self.laser_on = True
        self.over_tray = False
        self.grid_floor = 0
        self.create_navigator()

    def create_navigator(self):
        navigator_points = self.map_navigator_points()

        if self.laser_on:
            pixel_x = navigator_points["navigator_tip"][0]
            pixel_y = navigator_points["navigator_tip"][1]
            points = (
                (pixel_x, pixel_y - 5),
                (pixel_x, pixel_y + self.grid_z*8),
            )
            self.navigator_laser = self.root_canvas.canvas.create_line(*points, width=2, fill=Color.red)

        self.navigator_top = self.root_canvas.canvas.create_polygon(*navigator_points["navigator_top"], fill="#FFD18C", outline="")
        self.navigator_left = self.root_canvas.canvas.create_polygon(*navigator_points["navigator_left"], fill="#FFB545", outline="")
        self.navigator_right =self.root_canvas.canvas.create_polygon(*navigator_points["navigator_right"], fill="#EAA031", outline="")

        oval_points = self.map_oval_points(4)
        self.navigator_point = self.root_canvas.canvas.create_oval(*oval_points, fill=Color.red, outline='')

    def clear_navigator(self):
        self.root_canvas.canvas.delete(self.navigator_laser)
        self.root_canvas.canvas.delete(self.navigator_point)
        self.root_canvas.canvas.delete(self.navigator_top)
        self.root_canvas.canvas.delete(self.navigator_left)
        self.root_canvas.canvas.delete(self.navigator_right)

    def map_navigator_points(self):
        pixel_x, pixel_y = map_3D_to_2D(self.grid_x, self.grid_y, self.grid_z)

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

    def map_oval_points(self, pixel_size):
        if not self.over_tray:
            self.grid_floor = 0
        pixel_x, pixel_y = map_3D_to_2D(self.grid_x, self.grid_y, self.grid_floor)

        oval_points = (
            (pixel_x - pixel_size, pixel_y + pixel_size/2),
            (pixel_x + pixel_size, pixel_y - pixel_size/2)
        )
        return oval_points
        






class Button():
    """
    Button class
    """
    def create_click_area(self, x, y, w, h, shape):
        if shape == "rectangle":
            return self.root_canvas.canvas.create_rectangle(x, y, x+w, y+h, fill="", outline="")
        if shape == "oval":
            return self.root_canvas.canvas.create_oval(x, y, x+w, y+h, fill="", outline="")

class ToggleButton(Button):
    """
    ToggleButton class
    """
    def __init__(self, root_canvas, x, y, w, h, active_color, active_text, inactive_color, inactive_text, text_size, function):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.root_canvas = root_canvas
        self.active_color = active_color
        self.active_text  = active_text
        self.inactive_color = inactive_color
        self.inactive_text  = inactive_text
        self.text_size = text_size
        self.function = function
        self.status = "inactive"
        self.create_toggle_button()

    def clicked(self, event):
        if self.status == "inactive":
            self.status = "active"
        else:
            self.status = "inactive"
        self.function(self.status)
        # self.root_canvas.canvas.delete("all")
        self.create_toggle_button()

    def create_toggle_button(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        if self.status == "active":
            self.root_canvas.create_round_rectangle(x, y, w, h, h/2, self.active_color)
            self.root_canvas.canvas.create_oval(x+w-h+3, y+3, x+w-3, y+h-3, fill=Color.white, outline="")
        elif self.status == "inactive":
            self.root_canvas.create_round_rectangle(x, y, w, h, h/2, self.inactive_color)
            self.root_canvas.canvas.create_oval(x+3, y+3, x+h-3, y+h-3, fill=Color.white, outline="")  
        self.click_area = self.create_click_area(x, y, w, h, "rectangle")
        self.root_canvas.canvas.tag_bind(self.click_area, "<ButtonRelease-1>", self.clicked)