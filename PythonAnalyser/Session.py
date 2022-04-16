import numpy as np

import AppSettings


class Session:
    def __init__(self, file_prefix):
        file_prefix_split = file_prefix.split("_")
        self.IMEI = file_prefix_split[0].split("/")[-1]
        self.start_time = file_prefix_split[1]
        self.accel_filename = file_prefix + "_accel.txt"
        self.gyro_filename = file_prefix + "_gyro.txt"
        self.rota_filename = file_prefix + "_rota.txt"
        self.set_list_from_file()
        self.accels = self.accels[self.accels[:,0].argsort(kind='mergesort')]
        self.gyros = self.gyros[self.gyros[:,0].argsort(kind='mergesort')]
        self.rotas = self.rotas[self.rotas[:,0].argsort(kind='mergesort')]
        self.label = file_prefix_split[0].replace(AppSettings.get_model_data_dir(),"").replace(AppSettings.get_new_data_dir(),"").split("\\")[0]
        self.name = file_prefix_split[-1]

    @staticmethod
    def get_list_from_file(line):
        line = line.replace("\n","")
        ls = line.split(",")

        r = np.empty([len(ls)])
        for i in range(len(ls)):
            if i == 0:
                r[i] = np.longlong(ls[i])
            else:
                r[i] = float(ls[i])
        return r

    def set_list_from_file(self):
        accel_file = open(self.accel_filename, 'r')
        accel_lines = accel_file.readlines()
        self.accels = np.empty([len(accel_lines), 4])
        for i in range(len(accel_lines)):
            self.accels[i] = self.get_list_from_file(accel_lines[i])

        gyro_file = open(self.gyro_filename, 'r')
        gyro_lines = gyro_file.readlines()
        self.gyros = np.empty([len(gyro_lines), 4])
        for i in range(len(gyro_lines)):
            self.gyros[i] = self.get_list_from_file(gyro_lines[i])

        rota_file = open(self.rota_filename, 'r')
        rota_lines = rota_file.readlines()
        self.rotas = np.empty([len(rota_lines), 6])
        for i in range(len(rota_lines)):
            self.rotas[i] = self.get_list_from_file(rota_lines[i])