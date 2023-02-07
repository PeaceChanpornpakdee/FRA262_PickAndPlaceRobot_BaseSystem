import math

def map_3D_to_2D(grid_x, grid_y, grid_z):
    pixel_grid_offset_x = 20
    pixel_grid_offset_y = 120
    pixel_x = pixel_grid_offset_x +  8*(grid_x+15) - 8*(grid_y+35) + 560
    pixel_y = pixel_grid_offset_y - (4*(grid_x+15) + 4*(grid_y+35) - 400 + 8*grid_z)
    return pixel_x, pixel_y

def map_tray_points(grid_x, grid_y, tray_width, tray_height, tray_thick, orientation):
    tray_diagonal = (tray_width**2 + tray_height**2) ** 0.5
    theta = math.radians(orientation)
    tray_theta = math.atan(tray_width / tray_height)

    tray_points = {
        "bottom_tray" : (
            map_3D_to_2D( grid_x, grid_y, 0 ),
            map_3D_to_2D( grid_x + tray_width    * math.cos(theta),            grid_y - tray_width    * math.sin(theta),            0 ),
            map_3D_to_2D( grid_x + tray_diagonal * math.sin(theta+tray_theta), grid_y + tray_diagonal * math.cos(theta+tray_theta), 0 ),
            map_3D_to_2D( grid_x + tray_height   * math.sin(theta),            grid_y + tray_height   * math.cos(theta),            0 ),
        ),
        "top_tray" : (
            map_3D_to_2D( grid_x, grid_y, tray_thick ),
            map_3D_to_2D( grid_x + tray_width    * math.cos(theta),            grid_y - tray_width    * math.sin(theta), tray_thick ),
            map_3D_to_2D( grid_x + tray_diagonal * math.sin(theta+tray_theta), grid_y + tray_diagonal * math.cos(theta+tray_theta), tray_thick ),
            map_3D_to_2D( grid_x + tray_height   * math.sin(theta),            grid_y + tray_height   * math.cos(theta), tray_thick )
        ),
    }

    if orientation <= 45:
        left_side  = (3, 0)
        right_side = (0, 1) 
    elif orientation <= 135:
        left_side  = (0, 1)
        right_side = (1, 2) 
    elif orientation <= 225:
        left_side  = (1, 2)
        right_side = (2, 3) 
    elif orientation <= 315:
        left_side  = (2, 3)
        right_side = (3, 0) 
    else:
        left_side  = (3, 0)
        right_side = (0, 1) 

    tray_points["left_wall"] = ( 
        tray_points["bottom_tray"][left_side[0]], 
        tray_points["bottom_tray"][left_side[1]], 
        tray_points["top_tray"][left_side[1]], 
        tray_points["top_tray"][left_side[0]]
    )
    tray_points["right_wall"] = ( 
        tray_points["bottom_tray"][right_side[0]], 
        tray_points["bottom_tray"][right_side[1]], 
        tray_points["top_tray"][right_side[1]], 
        tray_points["top_tray"][right_side[0]]
    )

    return tray_points

def map_navigator_points(grid_x, grid_y, grid_z):
    pixel_x, pixel_y = map_3D_to_2D(grid_x, grid_y, grid_z)

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