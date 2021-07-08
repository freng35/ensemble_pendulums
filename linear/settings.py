
def get_ith_param(i):
    global array
    return array[i]


PROG_TITLE = "СЭЛФ: Ансамбль математических маятников"

SYSTEM_WINDOWS = "win32"
SYSTEM_MAC = "darwin"
SYSTEM_LINUX = "linux"

WINDOW_WIDTH_WIN = 1000
WINDOW_HEIGHT_WIN = 500
WINDOW_WIDTH_MAC = 1050
WINDOW_HEIGHT_MAC = 550

default_time = 0
default_length = 4
default_amplitude = 100
default_number_of_pendulums = 10
default_size = 10
default_delta_nu = 0.1

max_value = 25
max_delta = 10
min_delta = 0
min_value = 1

array = [default_amplitude, default_number_of_pendulums, default_size, default_delta_nu]
