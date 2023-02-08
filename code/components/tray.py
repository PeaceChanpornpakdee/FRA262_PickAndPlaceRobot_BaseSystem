from components.color import Color
import math

class Tray():
    """
    Tray class
    """
    def __init__(self, root_canvas, root_grid):
        self.root_canvas = root_canvas
        self.root_grid = root_grid
        self.origin_x = 0
        self.origin_y = 0
        self.orientation = 0
        self.tray_width = 6
        self.tray_height = 5
        self.tray_thick = 0.5
        self.create_tray()

    def create_tray(self):
        tray_points = self.map_tray_points()
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

    def map_tray_points(self):
        self.tray_diagonal = (self.tray_width**2 + self.tray_height**2) ** 0.5
        self.orientation = self.orientation % 360
        theta = math.radians(self.orientation)
        tray_theta = math.atan(self.tray_width / self.tray_height)

        tray_points = {
            "bottom_tray" : (
                self.root_grid.map_3D_to_2D( self.origin_x, self.origin_y, 0 ),
                self.root_grid.map_3D_to_2D( self.origin_x + self.tray_width    * math.cos(theta),            self.origin_y - self.tray_width    * math.sin(theta),            0 ),
                self.root_grid.map_3D_to_2D( self.origin_x + self.tray_diagonal * math.sin(theta+tray_theta), self.origin_y + self.tray_diagonal * math.cos(theta+tray_theta), 0 ),
                self.root_grid.map_3D_to_2D( self.origin_x + self.tray_height   * math.sin(theta),            self.origin_y + self.tray_height   * math.cos(theta),            0 ),
            ),
            "top_tray" : (
                self.root_grid.map_3D_to_2D( self.origin_x, self.origin_y, self.tray_thick ),
                self.root_grid.map_3D_to_2D( self.origin_x + self.tray_width    * math.cos(theta),            self.origin_y - self.tray_width    * math.sin(theta), self.tray_thick ),
                self.root_grid.map_3D_to_2D( self.origin_x + self.tray_diagonal * math.sin(theta+tray_theta), self.origin_y + self.tray_diagonal * math.cos(theta+tray_theta), self.tray_thick ),
                self.root_grid.map_3D_to_2D( self.origin_x + self.tray_height   * math.sin(theta),            self.origin_y + self.tray_height   * math.cos(theta), self.tray_thick )
            ),
        }

        if self.orientation <= 45:
            left_side  = (3, 0)
            right_side = (0, 1) 
        elif self.orientation <= 135:
            left_side  = (0, 1)
            right_side = (1, 2) 
        elif self.orientation <= 225:
            left_side  = (1, 2)
            right_side = (2, 3) 
        elif self.orientation <= 315:
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
                hole_centers[row].append( self.root_grid.map_3D_to_2D( self.origin_x + hole_diagonal * math.sin(theta+hole_theta), self.origin_y + hole_diagonal * math.cos(theta+hole_theta), self.tray_thick ), )

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