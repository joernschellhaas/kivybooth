import wiringpi
import time

LIGHT_PIN = 1

wiringpi.wiringPiSetup()
wiringpi.pinMode(LIGHT_PIN, wiringpi.PWM_OUTPUT)

while True:
    #for i in [*range(1024), *range(1024, 0, -1)]:
    #    wiringpi.pwmWrite(LIGHT_PIN, i)
    #    time.sleep(0.002)
    wiringpi.pwmWrite(LIGHT_PIN, 1024)
    time.sleep(0.5)
    wiringpi.pwmWrite(LIGHT_PIN, 0)
    time.sleep(2)
