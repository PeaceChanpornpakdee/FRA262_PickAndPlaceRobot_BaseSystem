class Keyboard():
    """
    Keyboard Class for Developer
    """
    def __init__(self, app):
        self.app = app
        
    def key_left(self, event):
        # self.app.navi.grid_x   -= 0.1
        self.app.navi.move_to(self.app.navi.grid_x-0.1, self.app.navi.grid_y)
        self.app.target.grid_x -= 0.1
    def key_right(self, event):
        # self.app.navi.grid_x   += 0.1
        self.app.navi.move_to(self.app.navi.grid_x+0.1, self.app.navi.grid_y)
        self.app.target.grid_x += 0.1
    def key_up(self, event):
        # self.app.navi.grid_y   += 0.1
        self.app.navi.move_to(self.app.navi.grid_x, self.app.navi.grid_y+0.1)
        self.app.target.grid_y += 0.1
    def key_down(self, event):
        # self.app.navi.grid_y   -= 0.1
        self.app.navi.move_to(self.app.navi.grid_x, self.app.navi.grid_y-0.1)
        self.app.target.grid_y -= 0.1
    # def key_k(self, event):
    #     self.app.navi.laser_on = False
    # def key_l(self, event):
    #     self.app.navi.laser_on = True

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
        # app.bind("<KeyPress-k>", self.key_k)
        # app.bind("<KeyPress-l>", self.key_l)
        app.bind("<KeyPress-a>", self.key_a)
        app.bind("<KeyPress-d>", self.key_d)
        app.bind("<KeyPress-w>", self.key_w)
        app.bind("<KeyPress-s>", self.key_s)
        app.bind("<KeyPress-q>", self.key_q)
        app.bind("<KeyPress-e>", self.key_e)