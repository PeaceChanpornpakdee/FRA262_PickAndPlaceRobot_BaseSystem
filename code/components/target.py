from components.color import Color

class Target():
    """
    Target class
    """
    def __init__(self, canvas, grid, grid_x, grid_y):
        self.canvas = canvas 
        self.grid = grid
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.create_target()

    def create_target(self):
        target_points = self.map_target_points()
        self.target_inner = self.canvas.create_oval(*target_points["inner_oval"], fill=Color.blue, outline='')
        self.target_outer = self.canvas.create_oval(*target_points["outer_oval"], fill='', outline=Color.blue, width=2)
        self.target_ticks = []
        for i in range(4):
            self.target_ticks.append(self.canvas.create_line(*target_points["tick"][i], fill=Color.blue, width=2))

    def clear_target(self):
        self.canvas.delete(self.target_inner)
        self.canvas.delete(self.target_outer)
        for i in range(4):
            self.canvas.delete(self.target_ticks[i])
    
    def map_target_points(self):
        pixel_x, pixel_y = self.grid.map_3D_to_2D(self.grid_x, self.grid_y, 0)
        target_points = {
            "inner_oval" : self.map_oval_points(4),
            "outer_oval" : self.map_oval_points(10),
            "tick" : [
                ((pixel_x+12, pixel_y+6), (pixel_x+8, pixel_y+4)),
                ((pixel_x+12, pixel_y-6), (pixel_x+8, pixel_y-4)),
                ((pixel_x-12, pixel_y-6), (pixel_x-8, pixel_y-4)),
                ((pixel_x-12, pixel_y+6), (pixel_x-8, pixel_y+4)),  
            ]
        }
        return target_points

    def map_oval_points(self, pixel_size):
        pixel_x, pixel_y = self.grid.map_3D_to_2D(self.grid_x, self.grid_y, 0)
        oval_points = (
            (pixel_x - pixel_size, pixel_y + pixel_size/2),
            (pixel_x + pixel_size, pixel_y - pixel_size/2)
        )
        return oval_points

    