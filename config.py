VEHICLE_VARIANT = 'current'  # current, future, tipping_point
MAP_RESOLUTION = 60
VALUE_CAPITAL = 10000
PROB_LOSS_PER_FLT_HR = 5e-3
CRUISE_SPEED = 28  # m/s
VALUE_PREVENTED_FATALITY = 2308000
DEBUG = False

# north: 50.9517765
# east: -1.3419628
# south: 50.9065510
# west: -1.4500237
LAT_BOUNDS = (50.907, 50.952)
LON_BOUNDS = (-1.450, -1.342)

def get_variant():
    return VEHICLE_VARIANT

def get_resolution():
    return MAP_RESOLUTION

def get_speed():
    return CRUISE_SPEED

def get_vpf():
    return VALUE_PREVENTED_FATALITY

