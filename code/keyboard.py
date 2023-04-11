class Keyboard():
    """
    Keyboard Class for Developer
    """
    def __init__(self, app):
        self.app = app

    def move_to(self, grid_x, grid_y):
        self.app.navi.move_to(grid_x, grid_y)
        pixel_x, pixel_y = self.app.grid.map_3D_to_2D(grid_x, grid_y, self.app.navi.grid_z)
        self.app.message_navi.move_to (pixel_x+14, pixel_y-10)
        self.app.message_laser.move_to(pixel_x+14, pixel_y+38)
        
    def key_left(self, event):
        self.move_to(self.app.navi.grid_x-0.5, self.app.navi.grid_y)
    def key_right(self, event):
        self.move_to(self.app.navi.grid_x+0.5, self.app.navi.grid_y)
    def key_up(self, event):
        self.move_to(self.app.navi.grid_x, self.app.navi.grid_y+0.5)
    def key_down(self, event):
        self.move_to(self.app.navi.grid_x, self.app.navi.grid_y-0.5)

    def key_a(self, event):
        self.app.tray_pick.origin_x -= 0.1
    def key_d(self, event):
        self.app.tray_pick.origin_x += 0.1
    def key_w(self, event):
        self.app.tray_pick.origin_y += 0.1
    def key_s(self, event):
        self.app.tray_pick.origin_y -= 0.1
    def key_q(self, event):
        self.app.tray_pick.orientation -= 1
    def key_e(self, event):
        self.app.tray_pick.orientation += 1

    def key_bind(self, app):
        app.bind("<KeyPress-Left>", self.key_left)
        app.bind("<KeyPress-Right>", self.key_right)
        app.bind("<KeyPress-Up>", self.key_up)
        app.bind("<KeyPress-Down>", self.key_down)
        app.bind("<KeyPress-a>", self.key_a)
        app.bind("<KeyPress-d>", self.key_d)
        app.bind("<KeyPress-w>", self.key_w)
        app.bind("<KeyPress-s>", self.key_s)
        app.bind("<KeyPress-q>", self.key_q)
        app.bind("<KeyPress-e>", self.key_e)