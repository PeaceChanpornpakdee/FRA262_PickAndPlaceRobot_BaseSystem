def laser_transmit(status):
    if status == "inactive":
        print("Turn Laser OFF")
    else:
        print("Turn Laser ON")

def hello():
    print("Hello")

def map_2D_to_3D(pixel_x, pixel_y):
    offset_x = 20
    offset_y = 120
    grid_x =  (pixel_x - 2*pixel_y - offset_x + 2*offset_y) / 16
    grid_y = -(pixel_x + 2*pixel_y - offset_x - 2*offset_y - 800) / 16
    if grid_x > 15:
        grid_x = 15
    elif grid_x < -15:
        grid_x = -15
    if grid_y > 35:
        grid_y = 35
    elif grid_y < -35:
        grid_y = -35

    print("grid:", grid_x, grid_y)
    return grid_x, grid_y

def mouse_position(event):
    print("pixel:", event.x, event.y)
    map_2D_to_3D(event.x, event.y)