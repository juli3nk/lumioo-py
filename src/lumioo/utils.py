
# Function to convert speed in m/s to km/h
def mps_to_kmph(mps):
    """
    1 km = 1000 m and 1 hr = 3600 sec (60 min x 60 sec each).

    Divide the speed by 1000 and multiply the result by 3600.
    1 m/sec = 18/5 km/hr or 3.6 km/hr
    """
    return round(3.6 * mps, 2)
