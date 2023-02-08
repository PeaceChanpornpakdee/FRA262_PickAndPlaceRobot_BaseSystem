def laser_transmit(status):
    if status == "inactive":
        print("Turn Laser OFF")
    else:
        print("Turn Laser ON")

def hello():
    print("Hello")

def mouse_position(event):
    print(event.x, event.y)