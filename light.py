import wiringpi
import time

LIGHT_PIN = 1

wiringpi.wiringPiSetup()
wiringpi.pinMode(LIGHT_PIN, wiringpi.PWM_OUTPUT)


def set_brightness(value):
    wiringpi.pwmWrite(LIGHT_PIN, int(1024 * value))


if __name__ == '__main__':
    # Test lights
    #for i in [*range(1024), *range(1024, 0, -1)]:
    #    wiringpi.pwmWrite(LIGHT_PIN, i)
    #    time.sleep(0.002)
    set_brightness(1)
    sleep(0.5)
    set_brightness(0)
