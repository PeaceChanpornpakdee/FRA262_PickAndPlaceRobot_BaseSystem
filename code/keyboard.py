import random

class Keyboard():
    """
    Keyboard Class for Developer
    """
    def __init__(self, app):
        self.app = app
        self.distance = 1

    def key_c(self, event):
        """
        This key function switches 'Connection'
        """
        self.app.new_connection = not self.app.connection

    def key_g(self, event):
        """
        This key function finishes 'Gripper' picking or placing
        """
        self.app.protocol_y.gripper_pick = "0"
        self.app.protocol_y.gripper_place = "0"

    def key_t(self, event):
        """
        This key function finishes 'Tray' picking or placing
        """
        self.app.protocol_y.pick_tray_origin_x = self.app.protocol_x.x_axis_actual_pos
        self.app.protocol_y.pick_tray_origin_y = self.app.protocol_y.y_axis_actual_pos
        self.app.protocol_y.pick_tray_orientation = random.uniform(0, 360)
        self.app.protocol_y.place_tray_origin_x = self.app.protocol_x.x_axis_actual_pos
        self.app.protocol_y.place_tray_origin_y = self.app.protocol_y.y_axis_actual_pos
        self.app.protocol_y.place_tray_orientation = random.uniform(0, 360)
        self.app.protocol_y.y_axis_moving_status = "Idle"

    def key_comma(self, event):
        if self.distance > 0.1:
            self.distance /= 10

    def key_dot(self, event):
        if self.distance < 10:
            self.distance *= 10
    
    def key_left(self, event):
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_x.x_axis_actual_pos > -150:
                pos = self.app.protocol_x.x_axis_actual_pos - self.distance
                self.app.protocol_x.x_axis_actual_pos = round(pos, 1)

    def key_right(self, event):
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_x.x_axis_actual_pos < 150:
                pos = self.app.protocol_x.x_axis_actual_pos + self.distance
                self.app.protocol_x.x_axis_actual_pos = round(pos, 1)

    def key_up(self, event):
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_y.y_axis_actual_pos < 350:
                pos = self.app.protocol_y.y_axis_actual_pos + self.distance
                self.app.protocol_y.y_axis_actual_pos = round(pos, 1)

    def key_down(self, event):
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_y.y_axis_actual_pos > -350:
                pos = self.app.protocol_y.y_axis_actual_pos - self.distance
                self.app.protocol_y.y_axis_actual_pos = round(pos, 1)



        
    # def move_to(self, grid_x, grid_y):
    #     self.app.navi.move_to(grid_x, grid_y)
    #     pixel_x, pixel_y = self.app.grid.map_3D_to_2D(grid_x, grid_y, self.app.navi.grid_z)
    #     if grid_x <= 0:
    #         # Message box = Navi's right
    #         self.app.message_navi.align = "Left"
    #         self.app.message_laser.align = "Left"
    #         self.app.message_navi.move_to (pixel_x+14, pixel_y-10)
    #         self.app.message_laser.move_to(pixel_x+14, pixel_y+38)
    #         self.app.message_navi.generate_tail_points()
    #         self.app.message_laser.generate_tail_points()
    #         self.app.message_navi.tail.recreate (self.app.message_navi.tail_points["NW"])
    #         self.app.message_laser.tail.recreate(self.app.message_laser.tail_points["SW"])
    #     else:
    #         # Message box = Navi's left
    #         self.app.message_navi.align = "Right"
    #         self.app.message_laser.align = "Right"
    #         self.app.message_navi.move_to (pixel_x-14, pixel_y-10)
    #         self.app.message_laser.move_to(pixel_x-14, pixel_y+38)
    #         self.app.message_navi.generate_tail_points()
    #         self.app.message_laser.generate_tail_points()
    #         self.app.message_navi.tail.recreate (self.app.message_navi.tail_points["NE"])
    #         self.app.message_laser.tail.recreate(self.app.message_laser.tail_points["SE"])

    

    # def key_a(self, event):
    #     self.app.tray_pick.origin_x -= 0.1
    # def key_d(self, event):
    #     self.app.tray_pick.origin_x += 0.1
    # def key_w(self, event):
    #     self.app.tray_pick.origin_y += 0.1
    # def key_s(self, event):
    #     self.app.tray_pick.origin_y -= 0.1
    # def key_q(self, event):
    #     self.app.tray_pick.orientation -= 1
    # def key_e(self, event):
    #     self.app.tray_pick.orientation += 1
    # def key_z(self, event):
    #     self.app.new_connection = False

    def key_bind(self, app):
        app.bind("<KeyPress-c>", self.key_c)
        app.bind("<KeyPress-g>", self.key_g)
        app.bind("<KeyPress-t>", self.key_t)
        app.bind("<KeyPress-,>", self.key_comma)
        app.bind("<KeyPress-.>", self.key_dot)
        app.bind("<KeyPress-Left>", self.key_left)
        app.bind("<KeyPress-Right>", self.key_right)
        app.bind("<KeyPress-Up>", self.key_up)
        app.bind("<KeyPress-Down>", self.key_down)
    #     app.bind("<KeyPress-a>", self.key_a)
    #     app.bind("<KeyPress-d>", self.key_d)
    #     app.bind("<KeyPress-w>", self.key_w)
    #     app.bind("<KeyPress-s>", self.key_s)
    #     app.bind("<KeyPress-q>", self.key_q)
    #     app.bind("<KeyPress-e>", self.key_e)
    #     app.bind("<KeyPress-z>", self.key_z)