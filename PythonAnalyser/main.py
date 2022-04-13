import Utilities
import AppSettings as set
from Sensors import SensorIn

if __name__ == '__main__':
    l = Utilities.get_filenames(set.get_new_data_dir())
    for x in range(len(l)):
        print(l[x])