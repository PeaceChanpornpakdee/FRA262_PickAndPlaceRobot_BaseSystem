import math

def map_3D_to_2D(grid_x, grid_y, grid_z):
    pixel_grid_offset_x = 20
    pixel_grid_offset_y = 120
    pixel_x = pixel_grid_offset_x +  8*(grid_x+15) - 8*(grid_y+35) + 560
    pixel_y = pixel_grid_offset_y - (4*(grid_x+15) + 4*(grid_y+35) - 400 + 8*grid_z)
    return pixel_x, pixel_y

def map_oval_points(grid_x, grid_y, grid_z, pixel_size):

    pixel_x, pixel_y = map_3D_to_2D(grid_x, grid_y, grid_z)

    oval_points = (
        (pixel_x - pixel_size, pixel_y + pixel_size/2),
        (pixel_x + pixel_size, pixel_y - pixel_size/2)
    )
    return oval_points

def map_target_points(grid_x, grid_y):
    pixel_x, pixel_y = map_3D_to_2D(grid_x, grid_y, 0)
    target_points = {
        "inner_oval" : map_oval_points(grid_x, grid_y, 0, 4),
        "outer_oval" : map_oval_points(grid_x, grid_y, 0, 10),
        "tick" : [
            ((pixel_x+12, pixel_y+6), (pixel_x+8, pixel_y+4)),
            ((pixel_x+12, pixel_y-6), (pixel_x+8, pixel_y-4)),
            ((pixel_x-12, pixel_y-6), (pixel_x-8, pixel_y-4)),
            ((pixel_x-12, pixel_y+6), (pixel_x-8, pixel_y+4)),  
        ]
    }
    return target_points