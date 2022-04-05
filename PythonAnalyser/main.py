from Sensors import SensorIn

if __name__ == '__main__':
    test = SensorIn.Session("358240051111110_1649168173746")
    print("Accel Values")
    for a in test.accels:
        print(str(a))
    print("Gyro Values")
    for g in test.gyros:
        print(str(g))
