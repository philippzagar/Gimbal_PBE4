# GPIO library
import RPi.GPIO as GPIO
# Math library
import math
# time library
import time
# MySQL library
from MySQL import *

class BLDC:
    # GPIO Pins
    # Enable Pins
    EN1 = 17
    EN2 = 27
    EN3 = 22
    en1 = None
    en2 = None
    en3 = None

    # Input Pins
    IN1 = 16
    IN2 = 20
    IN3 = 21
    in1 = None
    in2 = None
    in3 = None

    # Motor Direction
    direction = True

    # PWM Frequency
    pwm_freq = 3200

    # Sinus for every Phase
    x1 = 0.0
    x2 = (2 * math.pi) / 3
    x3 = (4 * math.pi) / 3
    sin1 = math.sin(x1)
    sin2 = math.sin(x2)
    sin3 = math.sin(x3)

    # Duty Cycle
    dc1 = 0
    dc2 = 0
    dc3 = 0

    # Database
    db = None

    now = None

    def __init__(self):
        # Open DB Conneciton
        db = Database()

        # Setup GPIO Pins
        GPIO.setmode(GPIO.BCM)
        # Setup Enable Pins
        GPIO.setup(self.EN1, GPIO.OUT)
        GPIO.setup(self.EN2, GPIO.OUT)
        GPIO.setup(self.EN3, GPIO.OUT)
        # Setup In Pins
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)

        # In Pins
        self.in1 = GPIO.PWM(self.IN1, self.pwm_freq)  # channel=12 frequency=50Hz
        self.in2 = GPIO.PWM(self.IN2, self.pwm_freq)  # channel=12 frequency=50Hz
        self.in3 = GPIO.PWM(self.IN3, self.pwm_freq)  # channel=12 frequency=50Hz

        # Duty Cycle
        self.dc1 = self.DC_Calculation(self.sin1)
        self.dc2 = self.DC_Calculation(self.sin2)
        self.dc3 = self.DC_Calculation(self.sin3)

        # Time
        self.now = time.time()

    def start(self):
        # Enable Pins
        self.en1 = GPIO.output(self.EN1, GPIO.HIGH)
        self.en2 = GPIO.output(self.EN2, GPIO.HIGH)
        self.en3 = GPIO.output(self.EN3, GPIO.HIGH)

        # Input Pins
        self.in1.start(self.dc1)
        self.in2.start(self.dc2)
        self.in3.start(self.dc3)

    def stop(self):
        # Enable Pins
        self.en1 = GPIO.output(self.EN1, GPIO.LOW)
        self.en2 = GPIO.output(self.EN2, GPIO.LOW)
        self.en3 = GPIO.output(self.EN3, GPIO.LOW)

        # Input Pins
        self.in1.stop(self.dc1)
        self.in2.stop(self.dc2)
        self.in3.stop(self.dc3)

    def run(self):
        # Calculate new Sinus Values
        self.Sinus_Calculate(0.1)

        # Duty Cycle
        self.dc1 = self.DC_Calculation(self.sin1)
        self.dc2 = self.DC_Calculation(self.sin2)
        self.dc3 = self.DC_Calculation(self.sin3)

        self.in1.ChangeDutyCycle(self.dc1)
        self.in2.ChangeDutyCycle(self.dc2)
        self.in3.ChangeDutyCycle(self.dc3)

    @staticmethod
    def DC_Calculation(sin):
        return 50 * sin + 50

    def Sinus_Calculate(self, step):
        self.x1 += step
        self.x2 += step
        self.x3 += step

        # Sinus for every Phase
        self.sin1 = math.sin(self.x1)
        self.sin2 = math.sin(self.x2)
        self.sin3 = math.sin(self.x3)

    def printSinusValues(self):
        print("Sin1:{0:.2f} Sin2:{1:.2f} Sin3:{2:.2f}".format(self.sin1, self.sin2, self.sin3))

        query = """
        INSERT INTO SinusValues
        (id, time, sin1, sin2, sin3)
        VALUES
        (NULL, {time}, {sin1}, {sin2}, {sin3});
        """

        # Insert query to DB
        # self.db.insert(query.format(time = time.time() - self.now, sin1 = self.sin1, sin2 = self.sin2, sin3 = self.sin3))

    def printDCValues(self):
        print("DC1:{0:.2f} DC2:{1:.2f} DC3:{2:.2f}".format(self.dc1, self.dc2, self.dc3))

        query = """
        INSERT INTO DCValues
        (id, time, dc1, dc2, dc3)
        VALUES
        (NULL, {time}, {dc1}, {dc2}, {dc3});
        """

        # Insert query to DB
        # self.db.insert(query.format(time = time.time() - self.now, dc1 = self.dc1, dc2 = self.dc2, dc3 = self.dc3))


    def __del__(self):
        # Cleanup GPIO Pins
        GPIO.cleanup()