#!/usr/bin/python

# I2C library
# import smbus
# math library
# import math
# time library
import time
# To import files from includes directory
# import sys
# import os
# sys.path.append(os.path.abspath("/home/pi/PBE4 Gimbal/includes"))
# MySQL library
from includes.MySQL import *
# MPU read library
from includes.functions import *

# Open DB Conneciton
db = Database()

now = time.time()

K = 0.98
K1 = 1 - K

time_diff = 0.01

# MPU Instance
mpu = MPU()

(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = mpu.read_all()

last_x = mpu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
last_y = mpu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

gyro_offset_x = gyro_scaled_x
gyro_offset_y = gyro_scaled_y

gyro_total_x = (last_x) - gyro_offset_x
gyro_total_y = (last_y) - gyro_offset_y

print("Time:{0:.4f} X_Last:{1:.2f} X_Total:{2:.2f} X_Last:{3:.2f} Y_Last:{4:.2f} Y_Total:{5:.2f} Y_Last:{6:.2f}"
      .format( time.time() - now, (last_x), gyro_total_x, (last_x), (last_y), gyro_total_y, (last_y)))

while 1:
    time.sleep(time_diff - 0.005)

    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = mpu.read_all()

    gyro_scaled_x -= gyro_offset_x
    gyro_scaled_y -= gyro_offset_y

    gyro_x_delta = (gyro_scaled_x * time_diff)
    gyro_y_delta = (gyro_scaled_y * time_diff)

    gyro_total_x += gyro_x_delta
    gyro_total_y += gyro_y_delta

    rotation_x = mpu.get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    rotation_y = mpu.get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)

    print("Time:{0:.2f} Pitch:{1:.1f} Roll:{2:.1f}".format(time.time() - now, (rotation_x), (rotation_y)))

    # Sin Values
    # print("Sin2:{0:.2f} Sin3:{1:.2f}").format(sin2, sin3)

    # Full Outprint
    # print("Time:{0:.2f} Pitch:{1:.1f} X_Total:{2:.1f} X_Last:{3:.1f} Roll:{4:.1f} Y_Total:{5:.1f} Y_Last:{6:.1f}"
    #      .format(time.time() - now, (rotation_x), (gyro_total_x), (last_x), (rotation_y), (gyro_total_y), (last_y)))

    query = """
        INSERT INTO testGyroData
        (id, dateTime, Time, Pitch, X_Total, X_Last, Roll, Y_Total, Y_Last, hex_adress)
        VALUES
        (NULL, {time}, {time_difference}, {rotation_x}, {gyro_total_x}, {last_x}, {rotation_y},
         {gyro_total_y}, {last_y}, {address});
        """

    #db.insert(query.format(time = time.time(), time_difference = time.time() - now, rotation_x=rotation_x, gyro_total_x=gyro_total_x, last_x=last_x, rotation_y=rotation_y,
    #                      gyro_total_y=gyro_total_y, last_y=last_y, address=address))