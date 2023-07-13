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
        """
        This key function decreases (<) distance by 10 times
        """
        if self.distance > 0.1:
            self.distance /= 10

    def key_dot(self, event):
        """
        This key function increases (>) distance by 10 times
        """
        if self.distance < 10:
            self.distance *= 10

    def key_slash(self, event):
        """
        This key function finishes moving
        """
        self.app.protocol_y.y_axis_moving_status = "Idle"
    
    def key_left(self, event):
        """
        This key function moving left
        """
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_x.x_axis_actual_pos > -150:
                pos = self.app.protocol_x.x_axis_actual_pos - self.distance
                self.app.protocol_x.x_axis_actual_pos = round(pos, 1)

    def key_right(self, event):
        """
        This key function moving right
        """
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_x.x_axis_actual_pos < 150:
                pos = self.app.protocol_x.x_axis_actual_pos + self.distance
                self.app.protocol_x.x_axis_actual_pos = round(pos, 1)

    def key_up(self, event):
        """
        This key function moving up
        """
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_y.y_axis_actual_pos < 350:
                pos = self.app.protocol_y.y_axis_actual_pos + self.distance
                self.app.protocol_y.y_axis_actual_pos = round(pos, 1)

    def key_down(self, event):
        """
        This key function moving down
        """
        if self.app.running or self.app.homing or self.app.jogging:
            if self.app.protocol_y.y_axis_actual_pos > -350:
                pos = self.app.protocol_y.y_axis_actual_pos - self.distance
                self.app.protocol_y.y_axis_actual_pos = round(pos, 1)

    def key_bind(self, app):
        """
        This function binds keyboard press with each key function
        """
        app.bind("<KeyPress-c>", self.key_c)
        app.bind("<KeyPress-g>", self.key_g)
        app.bind("<KeyPress-t>", self.key_t)
        app.bind("<KeyPress-,>", self.key_comma)
        app.bind("<KeyPress-.>", self.key_dot)
        app.bind("<KeyPress-/>", self.key_slash)
        app.bind("<KeyPress-Left>", self.key_left)
        app.bind("<KeyPress-Right>", self.key_right)
        app.bind("<KeyPress-Up>", self.key_up)
        app.bind("<KeyPress-Down>", self.key_down)

    def auto_pilot(self):
        """
        This functions auto pilot for point mode
        """
        distance_x = 0
        distance_y = 0
        
        diff_x = round(self.app.point_target_x - self.app.protocol_x.x_axis_actual_pos, 1)
        diff_y = round(self.app.point_target_y - self.app.protocol_y.y_axis_actual_pos, 1)
        
        if diff_x > 0:
            if diff_x > 1:          distance_x = 1
            elif diff_x >= 0.1:     distance_x = 0.1
        elif diff_x < 0:
            if diff_x < -1:         distance_x = -1
            elif diff_x <= -0.1:    distance_x = -0.1
        
        pos_x = self.app.protocol_x.x_axis_actual_pos + distance_x
        self.app.protocol_x.x_axis_actual_pos = round(pos_x, 1)

        if diff_y > 0:
            if diff_y > 1:          distance_y = 1
            elif diff_y >= 0.1:     distance_y = 0.1
        elif diff_y < 0:
            if diff_y < -1:         distance_y = -1
            elif diff_y <= -0.1:    distance_y = -0.1

        pos_y = self.app.protocol_y.y_axis_actual_pos + distance_y
        self.app.protocol_y.y_axis_actual_pos = round(pos_y, 1)