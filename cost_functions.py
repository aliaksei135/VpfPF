# FROM Andy:

# Current:
## Labour:          £175.64 / hour
## Vehicle Running: £32.40  / hour
## Vehicle Daily:   £8.99   / day

# Future (28% of current):
## Labour:          £31.44 / hour
## Vehicle Running: £20.33 / hour
## Vehicle Daily:   £8.99  / day

# Tipping Point (18.5% of current):
## Labour:          £32.49 / hour
## Vehicle Running: £5.99  / hour
## Vehicle Daily:   £1.66  / day


from bresenham import make_line
from config import get_variant, get_vpf, get_speed, get_resolution


def fixed_vehicle_costs():
    VARIANT = get_variant()
    if VARIANT == 'current' or VARIANT == 'future':
        return 8.99
    elif VARIANT == 'tipping_point':
        return 1.66


def marginal_vehicle_costs(seconds):
    hrs = seconds / 3600
    VARIANT = get_variant()
    if VARIANT == 'current':
        return (32.44 + 175.64) * hrs
    elif VARIANT == 'future':
        return (20.33 + 31.44) * hrs
    elif VARIANT == 'tipping_point':
        return (5.99 + 32.49) * hrs


def marginal_vpf_costs(grid, current, neighbour):
    VPF = get_vpf()
    # Check if current and neighbour are adjacent including diagonals
    if abs(current.x - neighbour.x) <= 1 and abs(current.y - neighbour.y) <= 1:
        return grid[neighbour.y][neighbour.x] * VPF
    else:
        path = make_line(current.x, current.y, neighbour.x, neighbour.y)
        return sum([grid[y][x] * VPF for y, x in path[1:]])


def total_marginal_costs(grid, current, neighbour):
    MAP_RESOLUTION = get_resolution()
    CRUISE_SPEED = get_speed()
    # Get euclidean distance between current and neighbour
    dist = ((current.x - neighbour.x) ** 2 + (current.y - neighbour.y) ** 2) ** 0.5
    time_between = (dist * MAP_RESOLUTION) / CRUISE_SPEED
    return marginal_vehicle_costs(time_between), marginal_vpf_costs(grid, current, neighbour)
