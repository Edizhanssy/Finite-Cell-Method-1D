
def map_local_to_global(local_coords, element_global_coords):
    global_start = element_global_coords[0] + local_coords[0] * (element_global_coords[1] - element_global_coords[0])
    global_end = element_global_coords[0] + local_coords[1] * (element_global_coords[1] - element_global_coords[0])

    return (global_start, global_end)
