import random
import time
import numpy as np

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M:00', prop)

def generate_new():
    layers = ["Test 1", "Test 2", "Test 3"]
    how_many_points = 1000
    data = {
        'globyte': {
            'pinpoints': [

            ]
        }
    }
    for layer in layers:
        for point in range(how_many_points):
            pinpoint = {
                'timestamp': random_date("2010-5-1 13:30:00", "2010-5-25 13:30:00", random.random()),
                'location': {
                    'lat': np.random.randint(-100, 100),
                    'long': np.random.randint(-100, 100)
                },
                'value': np.random.randint(1, 50),
                'layer': layer
            }
            data['globyte']['pinpoints'].append(pinpoint)
    
    return data


