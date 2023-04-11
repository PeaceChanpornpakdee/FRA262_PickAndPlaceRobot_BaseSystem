from components.color import Color
from components.shape import Polygon, FreeOval
import math

class Tray():
    """
    Tray class
    """
    def __init__(self, canvas, grid, navi):
        self.canvas = canvas
        self.grid = grid
        self.navi = navi
        self.origin_x = 0
        self.origin_y = 0
        self.orientation = 0
        self.tray_width = 6
        self.tray_height = 5
        self.tray_thick = 0.5
        self.create_tray()

    def create_tray(self):
        tray_points = self.map_tray_points()
        self.tray_bottom = Polygon(canvas=self.canvas, points=tray_points["bottom_tray"], color=Color.gray)
        self.tray_top    = Polygon(canvas=self.canvas, points=tray_points["top_tray"],    color=Color.lightgray)
        self.tray_left   = Polygon(canvas=self.canvas, points=tray_points["left_wall"],   color=Color.middlegray)
        self.tray_right  = Polygon(canvas=self.canvas, points=tray_points["right_wall"],  color=Color.gray)
        self.tray_holes  = []
        for row in range(3):
            for column in range(3):
                self.tray_holes.append(FreeOval(canvas=self.canvas, point_1=tray_points["holes"][row][column][0], point_2=tray_points["holes"][row][column][1], fill_color=Color.gray))
        self.navi_front()

    def navi_front(self):
        if self.navi != None:
            self.canvas.tag_raise(self.navi.navigator_laser.line, "all")
            self.canvas.tag_raise(self.navi.navigator_left.polygon, "all")
            self.canvas.tag_raise(self.navi.navigator_right.polygon, "all")
            self.canvas.tag_raise(self.navi.navigator_top.polygon, "all")
            self.canvas.tag_raise(self.navi.navigator_oval.free_oval, "all")

    def clear_tray(self):
        self.tray_top.clear()
        self.tray_bottom.clear()
        self.tray_left.clear()
        self.tray_right.clear()
        for i in range(9):
            self.tray_holes[i].clear()

    def map_tray_points(self):
        self.tray_diagonal = (self.tray_width**2 + self.tray_height**2) ** 0.5
        self.orientation = self.orientation % 360
        theta = math.radians(self.orientation)
        tray_theta = math.atan(self.tray_width / self.tray_height)

        tray_points = {
            "bottom_tray" : (
                self.grid.map_3D_to_2D( self.origin_x, self.origin_y, 0 ),
                self.grid.map_3D_to_2D( self.origin_x + self.tray_width    * math.cos(theta),            self.origin_y - self.tray_width    * math.sin(theta),            0 ),
                self.grid.map_3D_to_2D( self.origin_x + self.tray_diagonal * math.sin(theta+tray_theta), self.origin_y + self.tray_diagonal * math.cos(theta+tray_theta), 0 ),
                self.grid.map_3D_to_2D( self.origin_x + self.tray_height   * math.sin(theta),            self.origin_y + self.tray_height   * math.cos(theta),            0 ),
            ),
            "top_tray" : (
                self.grid.map_3D_to_2D( self.origin_x, self.origin_y, self.tray_thick ),
                self.grid.map_3D_to_2D( self.origin_x + self.tray_width    * math.cos(theta),            self.origin_y - self.tray_width    * math.sin(theta), self.tray_thick ),
                self.grid.map_3D_to_2D( self.origin_x + self.tray_diagonal * math.sin(theta+tray_theta), self.origin_y + self.tray_diagonal * math.cos(theta+tray_theta), self.tray_thick ),
                self.grid.map_3D_to_2D( self.origin_x + self.tray_height   * math.sin(theta),            self.origin_y + self.tray_height   * math.cos(theta), self.tray_thick )
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
                hole_centers[row].append( self.grid.map_3D_to_2D( self.origin_x + hole_diagonal * math.sin(theta+hole_theta), self.origin_y + hole_diagonal * math.cos(theta+hole_theta), self.tray_thick ), )

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