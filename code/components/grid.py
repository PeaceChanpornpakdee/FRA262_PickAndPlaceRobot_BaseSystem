class Grid():
    """
    Grid class
    root_canvas (canvas) : root canvas
    offset_x (int) : top left origin x
    offset_y (int) : top left origin y
    row (int)    : number of rows
    column (int) : number of columns
    color (str)  : color code 
    """
    def __init__(self, root_canvas, offset_x, offset_y, row, column, color):
        self.root_canvas = root_canvas
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.row = row
        self.column = column
        self.color = color
        self.create_grid()

    def create_grid(self):
        x = self.offset_x
        y = self.offset_y
        for r in range(self.row+1):
            self.root_canvas.canvas.create_line((x+560-8*r, y+280+120-4*r), (x+560+240-8*r, y+280-4*r), width=1, fill=self.color)

        for c in range(self.column+1):
            self.root_canvas.canvas.create_line((x+8*c, y+120-4*c), (x+560+8*c, y+120+280-4*c), width=1, fill=self.color)

        self.root_canvas.canvas.create_line((x+560-8*35, y+280+120-4*35), (x+560+240-8*35, y+280-4*35), width=2, fill=self.color)
        self.root_canvas.canvas.create_line((x+8*15, y+120-4*15), (x+560+8*15, y+120+280-4*15), width=2, fill=self.color)

    def map_3D_to_2D(self, grid_x, grid_y, grid_z):
        pixel_x = self.offset_x +  8*(grid_x+15) - 8*(grid_y+35) + 560
        pixel_y = self.offset_y - (4*(grid_x+15) + 4*(grid_y+35) - 400 + 8*grid_z)
        return pixel_x, pixel_y