import AppSettings as _set


class GyroIn:
    def __init__(self, line):
        split_line = line.split(",")
        self.timestamp = int(split_line[0])
        self.rx = float(split_line[1])
        self.ry = float(split_line[2])
        self.rz = float(split_line[3])

    def __str__(self):
        return str(self.timestamp) + "," + str(self.rx) + "," + str(self.ry) + "," + str(self.rz)


class AccelIn:
    def __init__(self, line):
        split_line = line.split(",")
        self.timestamp = int(split_line[0])
        self.tx = float(split_line[1])
        self.ty = float(split_line[2])
        self.tz = float(split_line[3])

    def __str__(self):
        return str(self.timestamp) + "," + str(self.tx) + "," + str(self.ty) + "," + str(self.tz)


class RotaIn:
    def __init__(self, line):
        split_line = line.split(",")
        self.timestamp = int(split_line[0])
        self.rx = float(split_line[1])
        self.ry = float(split_line[2])
        self.rz = float(split_line[3])
        self.v3 = float(split_line[4])
        self.v4 = float(split_line[5])

    def __str__(self):
        return str(self.timestamp) + "," + str(self.rx) + "," + str(self.ry) + "," + str(self.rz) + "," + str(self.v3) + "," + str(self.v4)


class Session:
    def __init__(self, file_prefix):
        file_prefix_split = file_prefix.split("_")
        self.IMEI = file_prefix_split[0]
        self.start_time = file_prefix_split[1]
        self.accel_filename = file_prefix + "_accel.txt"
        self.gyro_filename = file_prefix + "_gyro.txt"
        self.rota_filename = file_prefix + "_rota.txt"
        self.accels = list()
        self.gyros = list()
        self.rotas = list()
        self.set_list_from_file()
        self.accels = sorted(self.accels, key=lambda x: x.timestamp)
        self.gyros = sorted(self.gyros, key=lambda x: x.timestamp)
        self.rotas = sorted(self.rotas, key=lambda x: x.timestamp)

    def set_list_from_file(self):
        accel_file = open(_set.get_new_data_dir() + self.accel_filename, 'r')
        accel_lines = accel_file.readlines()
        for line in accel_lines:
            self.accels.append(AccelIn(line))
        gyro_file = open(_set.get_new_data_dir() + self.gyro_filename, 'r')
        gyro_lines = gyro_file.readlines()
        for line in gyro_lines:
            self.gyros.append(GyroIn(line))
        rota_file = open(_set.get_new_data_dir() + self.rota_filename, 'r')
        rota_lines = rota_file.readlines()
        for line in rota_lines:
            self.rota.append(GyroIn(line))