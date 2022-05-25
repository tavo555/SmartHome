# !/usr/bin/env python3
# ## ###############################################
#
# led_manager.py
# Controls leds in the GPIO
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################


import RPi.GPIO as GPIO
from time import sleep
import smbus2
import struct
# Arduino’s I2C device address
SLAVE_ADDR = 0x0A # I2C Address of Arduino 1

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)
class interval_exceeded_percent(Exception):
    def __init__(self, value ,mensaje=None):
        mensaje='\n The number {} exceeded the interval value of percent 20-100.'.format(value)#guarda mensaje
        super(interval_exceeded_percent,self).__init__(mensaje)
def readPower():
	try:
		# Creates a message object to read 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg) # Performs write
		data = list(msg) # Converts stream to list
		lista=bytes(data)
		pwr = struct.unpack('<f', lista)
		# print(’Received temp: {} = {}’.format(data, pwr))
		return pwr
	except:
		return None
def writePower(pwr):
	try:
		data = struct.pack('<f', pwr) # Packs number as float
		# Creates a message object to write 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg) 
		# Performs write	
	except:
		pass	

# Import Raspberry Pi's GPIO control library
GPIO.setwarnings(False)

""" Enciende el leds especificados en num, apagando los demás
	(To be developed by the student)
"""
GPIO.setmode(GPIO.BCM)
def get_timbre():
	GPIO.setup(17,GPIO.IN)
	input_state=GPIO.input(17)
	if input_state==True:
		timbre=1
		print("Boton presionado")
		sleep(0.2)
	else:
		timbre=0
	return timbre
def timbre():
	GPIO.setup(17,GPIO.IN)
	input_state=GPIO.input(17)
	if input_state==True:
		timbre=1
		print("Boton presionado")
		sleep(0.2)
	else:
		timbre=0


""" Enciende el leds especificados en num, apagando los demás
	(To be developed by the student)
"""
def focos(num):
	try:
		if(num==1):
			GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
			GPIO.output(18,0)  # Turn leds off
			sleep(1.0)
		else:
			GPIO.output(18,1)  # Turn leds off
			sleep(1.0)
	except:
		pass
def dimmer_start(pf_web):
	try:
		power_factor=int(pf_web)
		if power_factor >= 20 and power_factor <= 100:
			writePower(power_factor)
			print("\tPower set to {}".format(readPower()))
		else:
			print("\tInvalid!")
			raise interval_exceeded_percent(power_factor,None)#lanza excepcion
	except ValueError as verr:
			print("Warning:")
			print("Cannot convert int to string")
			print("Please enter only digits")
			help_example()
			return
	#si el porcentaje no esta entre 20 y 100
	except interval_exceeded_percent as ie:
			print(ie)
			return
	
