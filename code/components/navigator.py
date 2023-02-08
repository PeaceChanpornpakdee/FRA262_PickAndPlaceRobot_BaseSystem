from components.color import Color

class Navigator():
    """
    Navigator class
    """
    def __init__(self, root_canvas, root_grid, grid_x, grid_y, grid_z):
        self.root_canvas = root_canvas
        self.root_grid = root_grid
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
        pixel_x, pixel_y = self.root_grid.map_3D_to_2D(self.grid_x, self.grid_y, self.grid_z)

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
        pixel_x, pixel_y = self.root_grid.map_3D_to_2D(self.grid_x, self.grid_y, self.grid_floor)

        oval_points = (
            (pixel_x - pixel_size, pixel_y + pixel_size/2),
            (pixel_x + pixel_size, pixel_y - pixel_size/2)
        )
        return oval_points