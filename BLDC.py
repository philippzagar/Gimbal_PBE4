# GPIO library
import RPi.GPIO as GPIO
# Math library
import math
# time library
import time
# MySQL library
from includes.MySQL import *
# new library for increased PWM frequency
import pigpio

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
    IN4 = 26
    IN5 = 19
    IN6 = 13
    IN7 = 25
    IN8 = 24
    IN9 = 23

    # Motor Direction
    direction = True

    # PWM Frequency
    pwm_freq = 1000

    # Step Speed
    step = None

    # Sinus for every Phase
    sin1_value = 0.0
    sin2_value = (2 * math.pi) / 3
    sin3_value = (4 * math.pi) / 3
    sin4_value = 0.0
    sin5_value = (2 * math.pi) / 3
    sin6_value = (4 * math.pi) / 3
    sin7_value = 0.0
    sin8_value = (2 * math.pi) / 3
    sin9_value = (4 * math.pi) / 3
    sin1 = math.sin(sin1_value)
    sin2 = math.sin(sin2_value)
    sin3 = math.sin(sin3_value)
    sin4 = math.sin(sin4_value)
    sin5 = math.sin(sin5_value)
    sin6 = math.sin(sin6_value)
    sin7 = math.sin(sin7_value)
    sin8 = math.sin(sin8_value)
    sin9 = math.sin(sin9_value)

    # Duty Cycle
    dc1 = 0
    dc2 = 0
    dc3 = 0
    dc4 = 0
    dc5 = 0
    dc6 = 0
    dc7 = 0
    dc8 = 0
    dc9 = 0

    # Database
    db = None

    # Time
    now = None

    # Test with new library to increase PWM Frequency
    port1 = None
    port2 = None
    port3 = None
    port4 = None
    port5 = None
    port6 = None
    port7 = None
    port8 = None
    port9 = None

    def __init__(self):
        # Open DB Conneciton
        # db = Database()

        # Setup GPIO Pins
        GPIO.setmode(GPIO.BCM)
        # Setup Enable Pins
        GPIO.setup(self.EN1, GPIO.OUT)
        GPIO.setup(self.EN2, GPIO.OUT)
        GPIO.setup(self.EN3, GPIO.OUT)

        # PiGPIO
        self.port1 = pigpio.pi()
        self.port2 = pigpio.pi()
        self.port3 = pigpio.pi()
        self.port4 = pigpio.pi()
        self.port5 = pigpio.pi()
        self.port6 = pigpio.pi()
        self.port7 = pigpio.pi()
        self.port8 = pigpio.pi()
        self.port9 = pigpio.pi()

        # Set GPIO as Output
        self.port1.set_mode(self.IN1, pigpio.OUTPUT)
        self.port2.set_mode(self.IN2, pigpio.OUTPUT)
        self.port3.set_mode(self.IN3, pigpio.OUTPUT)
        self.port4.set_mode(self.IN4, pigpio.OUTPUT)
        self.port5.set_mode(self.IN5, pigpio.OUTPUT)
        self.port6.set_mode(self.IN6, pigpio.OUTPUT)
        self.port7.set_mode(self.IN7, pigpio.OUTPUT)
        self.port8.set_mode(self.IN8, pigpio.OUTPUT)
        self.port9.set_mode(self.IN9, pigpio.OUTPUT)

        # Duty Cycle
        self.dc1 = self.DC_Calculation(self.sin1)
        self.dc2 = self.DC_Calculation(self.sin2)
        self.dc3 = self.DC_Calculation(self.sin3)
        self.dc4 = self.DC_Calculation(self.sin4)
        self.dc5 = self.DC_Calculation(self.sin5)
        self.dc6 = self.DC_Calculation(self.sin6)
        self.dc7 = self.DC_Calculation(self.sin7)
        self.dc8 = self.DC_Calculation(self.sin8)
        self.dc9 = self.DC_Calculation(self.sin9)

        # Time
        self.now = time.time()

        # Step
        self.step = 0.01

    def start_pigpio(self):
        # Enable Pins
        self.en1 = GPIO.output(self.EN1, GPIO.HIGH)
        self.en2 = GPIO.output(self.EN2, GPIO.HIGH)
        self.en3 = GPIO.output(self.EN3, GPIO.HIGH)

        self.port1.set_PWM_frequency(self.IN1,100000)
        self.port1.set_PWM_range(self.IN1, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port1.set_PWM_dutycycle(self.IN1, self.dc1) # PWM 1/2 on

        self.port2.set_PWM_frequency(self.IN2,100000)
        self.port2.set_PWM_range(self.IN2, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port2.set_PWM_dutycycle(self.IN2, self.dc2) # PWM 1/2 on

        self.port3.set_PWM_frequency(self.IN3,100000)
        self.port3.set_PWM_range(self.IN3, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port3.set_PWM_dutycycle(self.IN3, self.dc3) # PWM 1/2 on

        self.port4.set_PWM_frequency(self.IN4,100000)
        self.port4.set_PWM_range(self.IN4, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port4.set_PWM_dutycycle(self.IN4, self.dc4) # PWM 1/2 on

        self.port5.set_PWM_frequency(self.IN5,100000)
        self.port5.set_PWM_range(self.IN5, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port5.set_PWM_dutycycle(self.IN5, self.dc5) # PWM 1/2 on

        self.port6.set_PWM_frequency(self.IN6,100000)
        self.port6.set_PWM_range(self.IN6, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port6.set_PWM_dutycycle(self.IN6, self.dc6) # PWM 1/2 on

        self.port7.set_PWM_frequency(self.IN7,100000)
        self.port7.set_PWM_range(self.IN7, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port7.set_PWM_dutycycle(self.IN7, self.dc7) # PWM 1/2 on

        self.port8.set_PWM_frequency(self.IN8,100000)
        self.port8.set_PWM_range(self.IN8, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port8.set_PWM_dutycycle(self.IN8, self.dc8) # PWM 1/2 on

        self.port9.set_PWM_frequency(self.IN9,100000)
        self.port9.set_PWM_range(self.IN9, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port9.set_PWM_dutycycle(self.IN9, self.dc9) # PWM 1/2 on

    def run_pigpio(self):
        # Calculate new Sinus Values
        # with 0.1: pro 2*PI aendert sich PWM 62 Mal

        self.Sinus_Calculate()

        # Duty Cycle
        self.dc1 = self.DC_Calculation(self.sin1)
        self.dc2 = self.DC_Calculation(self.sin2)
        self.dc3 = self.DC_Calculation(self.sin3)
        self.dc4 = self.DC_Calculation(self.sin4)
        self.dc5 = self.DC_Calculation(self.sin5)
        self.dc6 = self.DC_Calculation(self.sin6)
        self.dc7 = self.DC_Calculation(self.sin7)
        self.dc8 = self.DC_Calculation(self.sin8)
        self.dc9 = self.DC_Calculation(self.sin9)

        self.port1.set_PWM_dutycycle(self.IN1, self.dc1)
        self.port2.set_PWM_dutycycle(self.IN2, self.dc2)
        self.port3.set_PWM_dutycycle(self.IN3, self.dc3)
        self.port4.set_PWM_dutycycle(self.IN4, self.dc4)
        self.port5.set_PWM_dutycycle(self.IN5, self.dc5)
        self.port6.set_PWM_dutycycle(self.IN6, self.dc6)
        self.port7.set_PWM_dutycycle(self.IN7, self.dc7)
        self.port8.set_PWM_dutycycle(self.IN8, self.dc8)
        self.port9.set_PWM_dutycycle(self.IN9, self.dc9)

    def stop_pigpio(self):
        # Enable Pins
        self.en1 = GPIO.output(self.EN1, GPIO.LOW)
        self.en2 = GPIO.output(self.EN2, GPIO.LOW)
        self.en3 = GPIO.output(self.EN3, GPIO.LOW)

    def test_BLDC(self):
        # Enable Pins
        self.en1 = GPIO.output(self.EN1, GPIO.HIGH)
        self.en2 = GPIO.output(self.EN2, GPIO.HIGH)
        self.en3 = GPIO.output(self.EN3, GPIO.HIGH)

        self.port1.set_PWM_frequency(self.IN1,100000)
        self.port1.set_PWM_range(self.IN1, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port1.set_PWM_dutycycle(self.IN1, 100) # PWM 1/2 on

        self.port2.set_PWM_frequency(self.IN2,100000)
        self.port2.set_PWM_range(self.IN2, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port2.set_PWM_dutycycle(self.IN2, 100) # PWM 1/2 on

        self.port3.set_PWM_frequency(self.IN3,100000)
        self.port3.set_PWM_range(self.IN3, 100)  # now  25 1/4,   50 1/2,   75 3/4 on
        self.port3.set_PWM_dutycycle(self.IN3, 100) # PWM 1/2 on

    def reverseRotation(self):
        if(self.direction == True):
            self.direction = False
        else:
            self.direction = True

    def changeSpeed(self, speed):
        self.step = speed

    @staticmethod
    def DC_Calculation(sin):
        return 50 * sin + 50

    def Sinus_Calculate(self):
        # Increase x values by step
        self.sin1_value += self.step
        self.sin2_value += self.step
        self.sin3_value += self.step
        self.sin4_value += self.step
        self.sin5_value += self.step
        self.sin6_value += self.step
        self.sin7_value += self.step
        self.sin8_value += self.step
        self.sin9_value += self.step

        # Sinus for every Phase
        self.sin1 = math.sin(self.sin1_value)
        self.sin2 = math.sin(self.sin2_value)
        self.sin3 = math.sin(self.sin3_value)
        self.sin4 = math.sin(self.sin4_value)
        self.sin5 = math.sin(self.sin5_value)
        self.sin6 = math.sin(self.sin6_value)
        self.sin7 = math.sin(self.sin7_value)
        self.sin8 = math.sin(self.sin8_value)
        self.sin9 = math.sin(self.sin9_value)

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
        print("DC1:{0:.2f} DC2:{1:.2f} DC3:{2:.2f} DC4:{3:.2f} DC5:{4:.2f} DC6:{5:.2f} DC7:{6:.2f} DC8:{7:.2f} DC9:{8:.2f}"
              .format(self.dc1, self.dc2, self.dc3, self.dc4, self.dc5, self.dc6, self.dc7, self.dc8, self.dc9))

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
        self.port1.stop()
        self.port2.stop()
        self.port3.stop()
        self.port4.stop()
        self.port5.stop()
        self.port6.stop()
        self.port7.stop()
        self.port8.stop()
        self.port9.stop()
