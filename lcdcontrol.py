import serial
import time

class LCDControl(object):

    LINE_LENGTH = 16

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.led_state = True
        try:
	    self.port = serial.Serial(port, baudrate=baudrate)
	except:
	    self.port = file('/dev/null', 'w');

    def set_led(self, state):
        self.led_state = state
        self.port.write("3;{0};\r".format('1' if state else '0'))

    def blink(self, times=3):
        for i in range(times*2):
            self.set_led(not self.led_state)
            time.sleep(0.5)

    def set_text(self, line1, line2):
        if len(line1) > LCDControl.LINE_LENGTH: line1 = line1[0:LCDControl.LINE_LENGTH]
        if len(line2) > LCDControl.LINE_LENGTH: line2 = line1[0:LCDControl.LINE_LENGTH]
        self.port.write("1;1;{0}\r".format(line1))
        self.port.write("1;2;{0}\r".format(line2))

    def close(self):
        self.port.close()
