#!/usr/bin/python

# I2C library
# import smbus
# math library
# import math
# time library
import time
# GPIO library
import RPi.GPIO as GPIO
# MySQL library
from includes.MySQL import *
# MPU read library
from includes.functions import *

# GPIO Pins
EN1 = 17
EN2 = 27
EN3 = 22

IN1 = 16
IN2 = 20
IN3 = 21

# Motor Direction
direction = True

# Sinus for every Phase
sin1 = 0.0
sin2 = math.sin((2*math.pi) / 3)
sin3 = math.sin((4*math.pi) / 3)

# x Value for Sinus Function
x = 0.0

# Open DB Conneciton
db = Database()

# Setup GPIO Pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

p1 = GPIO.PWM(13, 50)  # channel=12 frequency=50Hz
p2 = GPIO.PWM(19, 50)  # channel=12 frequency=50Hz
p3 = GPIO.PWM(26, 50)  # channel=12 frequency=50Hz

p1.start(0)
p2.start(0)
p3.start(0)

now = time.time()

K = 0.98
K1 = 1 - K

time_diff = 0.01

(gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

gyro_offset_x = gyro_scaled_x
gyro_offset_y = gyro_scaled_y

gyro_total_x = (last_x) - gyro_offset_x
gyro_total_y = (last_y) - gyro_offset_y

print("Time:{0:.4f} X_Last:{1:.2f} X_Total:{2:.2f} X_Last:{3:.2f} Y_Last:{4:.2f} Y_Total:{5:.2f} Y_Last:{6:.2f}"
      .format( time.time() - now, (last_x), gyro_total_x, (last_x), (last_y), gyro_total_y, (last_y)))

while 1:
    time.sleep(time_diff - 0.005)

    (gyro_scaled_x, gyro_scaled_y, gyro_scaled_z, accel_scaled_x, accel_scaled_y, accel_scaled_z) = read_all()

    gyro_scaled_x -= gyro_offset_x
    gyro_scaled_y -= gyro_offset_y

    gyro_x_delta = (gyro_scaled_x * time_diff)
    gyro_y_delta = (gyro_scaled_y * time_diff)

    gyro_total_x += gyro_x_delta
    gyro_total_y += gyro_y_delta

    rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)

    print("Time:{0:.2f} Pitch:{1:.1f} X_Total:{2:.1f} X_Last:{3:.1f} Roll:{4:.1f} Y_Total:{5:.1f} Y_Last:{6:.1f}"
          .format(time.time() - now, (rotation_x), (gyro_total_x), (last_x), (rotation_y), (gyro_total_y), (last_y)))

    query = """
        INSERT INTO testGyroData
        (id, dateTime, Time, Pitch, X_Total, X_Last, Roll, Y_Total, Y_Last, hex_adress)
        VALUES
        (NULL, {time}, {time_difference}, {rotation_x}, {gyro_total_x}, {last_x}, {rotation_y},
         {gyro_total_y}, {last_y}, {address});
        """

    #db.insert(query.format(time = time.time(), time_difference = time.time() - now, rotation_x=rotation_x, gyro_total_x=gyro_total_x, last_x=last_x, rotation_y=rotation_y,
    #                      gyro_total_y=gyro_total_y, last_y=last_y, address=address))
# Stop GPIO Pins
p1.stop()
p2.stop()
p3.stop()

# Cleanup GPIO Pins
GPIO.cleanup()